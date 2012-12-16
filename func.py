# -*- coding: utf-8 -*-
import os
import time
from setting import *

def get_path(filename):
    if filename[:1] == '/':
        filename = filename[1:]
    abs_filename = os.path.abspath(template_dir + '/themes/' + theme + '/' + filename)
    return "/static/themes/%s/%s?v=%s" % (theme, filename, _file_version(abs_filename))


def _file_version(filename):
    try:
        secs = os.stat(filename).st_mtime
        t = time.localtime(secs)
        return str(time.strftime("%Y%m%d%H%M%S", t))
    except:
        return '0'

# Test
if __name__ == "__main__":
    print get_path('test.html')
    print get_path('/test.html')