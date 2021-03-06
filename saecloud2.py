#!D:\Dev\Python27\python.exe

import os
import sys
import yaml
import json
import shutil
import filecmp
import subprocess
import argparse
import os.path
import base64
import hmac
import hashlib
import urllib
import urllib2

SVN_EXE = "D:\\Dev\\Apache-Subversion-1.7.7\\bin\\svn.exe"

UPLOAD_SERVER = 'http://upload.sae.sina.com.cn'
DEPLOY_SERVER = 'http://deploy.sae.sina.com.cn'
SVN_SERVER = 'https://svn.sinaapp.com/'
LOCAL_CACHE_DIR = os.path.expanduser('~/.saecloud')

VERSION = '0.0.1'
verbose = False

def version(args):
    print "SAE command line v%s" % VERSION


def run(*args):
    # FIXME: Check the return code please
    if verbose:
        print '+', ' '.join(args)
        return subprocess.call(args, close_fds=True)
    else:
        return subprocess.call(args, close_fds=False, stdout=open(os.devnull, 'w'))


def _get_svn_opts(args):
    # opts = ['--username', SVN_USERNAME, '--password', SVN_PASSWORD]

    global SVN_EXE
    value = getattr(args, "svnexepath")
    if value:
        SVN_EXE = value
    print SVN_EXE

    opts = []
    for opt in ['username', 'password']:
        value = getattr(args, opt)
        if value:
            opts.append('--' + opt)
            opts.append(value)

    print opts
    return opts


def deploy(args):
    """Deploy local source to server

    Deploy code in source directory to sae server, by default source is current
    directory, version number is set in config.yaml. 

    """
    source = args.dir
    opts = _get_svn_opts(args)
    cache = LOCAL_CACHE_DIR

    conf_file = os.path.join(source, 'config.yaml')
    try:
        conf = yaml.load(open(conf_file))
    except:
        print >> sys.stderr, 'Error: Failed to load config.yaml'
        return

    name = conf['name']
    version = conf['version']

    print 'Deploying http://%s.%s.sinaapp.com' % (version, name)
    print 'Updating cache'
    name = str(name)
    path = os.path.join(cache, name)
    if not os.path.exists(path):
        url = SVN_SERVER + name
        run(SVN_EXE, 'checkout', url, path, *opts)
    else:
        run(SVN_EXE, 'update', path, '-q')

    print 'Finding changes'
    modified = False
    vpath = os.path.join(path, str(version))
    if os.path.exists(vpath):
        q = ['', ]
        while len(q):
            part = q.pop(0)
            s = os.path.join(source, part)
            t = os.path.join(vpath, part)
            dc = filecmp.dircmp(s, t, ['.svn'])

            # New files
            for f in dc.left_only:
                if f.startswith('.'):
                    continue
                d1 = os.path.join(s, f)
                d2 = os.path.join(t, f)
                if os.path.isdir(d1):
                    shutil.copytree(d1, d2)
                else:
                    shutil.copy2(d1, d2)
                run(SVN_EXE, 'add', d2, '-q')
                modified = True

            # Deleted files
            for f in dc.right_only:
                if f.startswith('.'):
                    continue
                d = os.path.join(t, f)
                if os.path.isdir(d):
                    shutil.rmtree(d)
                else:
                    os.unlink(d)
                run(SVN_EXE, 'delete', d, '-q')
                modified = True

            # Modified files
            for f in dc.diff_files:
                if f.startswith('.'):
                    continue
                d1 = os.path.join(s, f)
                d2 = os.path.join(t, f)
                shutil.copy2(d1, d2)
                modified = True

            subdirs = filter(lambda x: not x.startswith('.'), dc.common_dirs)
            q.extend([os.path.join(part, d) for d in subdirs])
    else:
        # New version
        shutil.copytree(source, vpath, ignore=shutil.ignore_patterns('.*'))
        run(SVN_EXE, 'add', vpath, '-q')
        modified = True

    if not modified:
        print 'No changes found',
        return
    print 'Pushing to server... ',
    sys.stdout.flush()
    run(SVN_EXE, 'commit', path, '-mx')
    print 'done'


def export(args):
    """Export source from sae server

    Export source currently deployed on the sae server to currently directory.
    Version 1 will be used unless you have specified a version number, also, 
    you can specify your svn username and password just as `saecloud depoly`

    """
    url = SVN_SERVER + args.app + '/' + args.version
    print 'Exporting to', args.app
    opts = _get_svn_opts(args)
    run(SVN_EXE, 'export', url, args.app, *opts)

ESC = "\x1b"
save = ESC + "7"
unsave = ESC + "8"
clear = ESC + "[2J"
erase_to_start = ESC + "[1K"

def setprogress(text, frac):
    if sys.stdout.isatty():
        sys.stdout.write(erase_to_start)
        sys.stdout.write(unsave)

    sys.stdout.write("%s ... %d%%" % (text, int(100 * frac)))
    if not sys.stdout.isatty():
        sys.stdout.write(os.linesep)

    sys.stdout.flush()


def uploadfile2(filename, appinfo, domain):
    offset = 0
    chunk_size = 1024 * 256
    token = '0'

    file_size = os.stat(filename).st_size

    appname, accesskey, secretkey = appinfo

    _domain = '%s-%s' % (appname, domain)
    fixed_headers = {
        'FileName': os.path.basename(filename),
        'FileSize': file_size,
        'Extra': 'storengine: stor; acl: reserve; domain: %s' % _domain,
        'User-Agent': 'SaeSdk',
        'AccessKey': accesskey,
    }

    def get_signature(key, msg):
        h = hmac.new(key, msg, hashlib.sha256)
        return base64.b64encode(h.digest())

    upload_file = open(filename)
    while True:
        upload_file.seek(offset)
        c = upload_file.read(chunk_size)
        checksum = hashlib.md5(c).hexdigest()

        end = min(offset + chunk_size, file_size)
        headers = {
            'FileRange': '%d-%d' % (offset, end),
            'FileRangeChecksum': checksum,
            'Signature': get_signature(secretkey, checksum),
            'Token': token,
            'Content-type': 'application/octet-stream',
            'Content-length': len(c),
        }
        headers.update(fixed_headers)

        url = UPLOAD_SERVER + '/uploader'
        req = urllib2.Request(url, c, headers)

        try:
            rep = urllib2.urlopen(req, None, 5).read()
        except urllib2.URLError, e:
            continue

        code, message = rep.split(':', 1)

        if code == '0':
            token = message
        elif code == '1':
            # upload finished finally
            break
        else:
            raise Exception("Server returned: %s" % rep)

        offset += chunk_size

        setprogress("Uploading %s" % filename, float(end) / file_size)

    setprogress("Uploading %s" % filename, 1.0)

    print


class LocalAuthData:
    def __init__(self, appname):
        self.appname = appname
        self.filename = hashlib.md5(appname).hexdigest()
        self.dir = os.path.join(LOCAL_CACHE_DIR, '.auth')
        self.path = os.path.join(self.dir, self.filename)

    def load(self):
        try:
            return json.load(open(self.path))
        except:
            return None

    def dump(self, dict):
        try:
            os.makedirs(self.dir)
        except:
            pass

        try:
            json.dump(dict, open(self.path, 'w'))
        except:
            pass

    def clear(self):
        try:
            os.unlink(self.path)
        except:
            pass


def upload_data(args):
    appname = args.app
    domain = args.domain
    files = args.file
    username = args.username
    password = args.password

    if username is None or password is None:
        conf = LocalAuthData(appname).load()
        if conf:
            username = conf['username']
            password = conf['password']
        else:
            # Try to read from STDIN
            username = raw_input("Username: ")
            import getpass

            password = getpass.getpass("Password: ")

    print "User authentication"
    params = urllib.urlencode([
        ('action', 'auth'), ('email', username), ('password', password)
    ])
    url = DEPLOY_SERVER + '/?' + params
    cookie = urllib2.urlopen(url).read()
    if cookie.find('\n') != -1:
        LocalAuthData(appname).clear()
        raise Exception(cookie.replace('\n', ' '))

    # If passed, saved the auth info in .saecloud
    LocalAuthData(appname).dump({
        'username': username, 'password': password
    })

    print "Getting application's information"
    params = urllib.urlencode([
        ('action', 'appinfo'), ('name', appname), ('cookie', cookie)
    ])
    url = DEPLOY_SERVER + '/?' + params
    rep = urllib2.urlopen(url).read()

    lines = rep.split('\n')
    code = lines[0].split()[0]
    if code == '0':
        _, accesskey, secretkey = lines[1].split()[:3]
    else:
        raise Exception(lines[1])

    print

    for f in files:
        uploadfile2(f, (appname, accesskey, secretkey), domain)


def install(args):
    dest = os.path.join(os.getcwd(), 'site-packages')

    if not os.path.exists(dest):
        os.mkdir(dest)

    import tempfile

    tmpdir = tempfile.gettempdir()
    argv = ['install', '-I',
            '--install-option=--install-lib=%s' % dest,
            '--install-option=--install-data=%s' % dest,
            '--install-option=--install-scripts=%s' % tmpdir]
    # only compile if it is python2.7.3
    import imp

    magic = imp.get_magic()[:2]
    if magic != '\x03\xf3':
        argv.append('--install-option=--no-compile')
    argv.extend(args.package)

    # In virtualenv, the install command will remove the old installed
    # distribution, patch to skip it.
    try:
        def _(*arg, **kws):
            pass

        import pip.req

        pip.req.InstallRequirement.uninstall = _
        pip.req.InstallRequirement.commit_uninstall = _
    except:
        pass

    import pip

    pip.main(argv)

    for f in os.listdir(dest):
        pth = os.path.join(dest, f)
        if os.path.isfile(pth) and f.endswith('.egg'):
            print 'uncompress: %s' % f
            import zipfile

            zf = zipfile.ZipFile(pth)
            zf.extractall(dest)
            zf.close()
            os.unlink(pth)


def main():
    parser = argparse.ArgumentParser(prog=os.path.basename(sys.argv[0]))
    parser.set_defaults(verbose=False)

    subparsers = parser.add_subparsers(help='sub commands')

    credentials = argparse.ArgumentParser(add_help=False)
    credentials.add_argument('-svn', '--svnexepath', help='path of svn.exe')
    credentials.add_argument('-u', '--username', help='repo username')
    credentials.add_argument('-p', '--password', help='repo password')
    credentials.add_argument('-v', '--verbose', dest='verbose', action='store_true',
        help='show lowlevel repo operations')

    p = subparsers.add_parser('export', parents=[credentials],
        help='export source code to local directory')
    p.add_argument('app', help='application name')
    p.add_argument('version', nargs='?', default='1',
        help='which version to export, default to 1')
    p.set_defaults(func=export)

    p = subparsers.add_parser('deploy', parents=[credentials],
        help='deploy source directory to SAE')
    p.add_argument('dir', nargs='?', default='.',
        help='the source code directory to deploy, default to current dir')
    p.set_defaults(func=deploy)

    p = subparsers.add_parser('install',
        help='helper to install packages for SAE application')
    p.add_argument('package', nargs='+', help='package name to install')
    p.set_defaults(func=install)

    p = subparsers.add_parser('upload-data', parents=[credentials],
        help='upload files to storage')
    p.add_argument('app', help='application name')
    p.add_argument('domain', help='storage domain name')
    p.add_argument('file', nargs='+', help='local files to upload')
    p.set_defaults(func=upload_data)

    p = subparsers.add_parser('version', help='show version info')
    p.set_defaults(func=version)

    args = parser.parse_args()
    global verbose
    if args.verbose: verbose = True

    args.func(args)

if __name__ == '__main__':
    main()
