# -*- coding: utf-8 -*-
import os
import time
from setting import *

def theme_path(filename):
    if filename[:1] == '/':
        filename = filename[1:]
    if not filename.startswith(theme_admin + '/'):
        filename = '%s/%s' % (theme, filename)
    return filename
    
def static_path(filename):
    filename = theme_path(filename)
    abs_filename = os.path.abspath(template_dir + '/' + filename)
    return "/static/%s?v=%s" % (filename, _file_version(abs_filename))

def _file_version(filename):
    try:
        secs = os.stat(filename).st_mtime
        t = time.localtime(secs)
        return str(time.strftime("%Y%m%d%H%M%S", t))
    except:
        return '0'

# Test
if __name__ == "__main__":
    print theme_path('test.html')
    print theme_path('/test.html')
    print theme_path('admin/test.html')
    
    print static_path('test.html')
    print static_path('/test.html')
    print static_path('admin/test.html')