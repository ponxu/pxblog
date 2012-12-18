# -*- coding: utf-8 -*-
import os
import time
from setting import *

def bloginfo(name):
    return 'bloginfo-%s' % name


def get_posts(paged, max=page_size):
    return [2,3,4,8,9]


def get_pages(max=page_size):
    return [2,3,4,8,9]


def get_tags():
    return [2,3,4,8,9]


# 带上theme, 如果以<theme_admin>开头, 不加theme
def theme_path(filename):
    if filename[:1] == '/':
        filename = filename[1:]
    if not filename.startswith(theme_admin + '/'):
        filename = '%s/%s' % (theme, filename)
    return filename


# 生成静态url
def static_path(filename, with_version=False):
    filename = theme_path(filename)
    if with_version:
        abs_filename = os.path.abspath(template_dir + '/' + filename)
        return "/static/%s?v=%s" % (filename, _file_version(abs_filename))
    else:
        return "/static/%s" % filename
    
    
def _file_version(filename):
    try:
        secs = os.stat(filename).st_mtime
        t = time.localtime(secs)
        return str(time.strftime("%Y%m%d%H%M%S", t))
    except:
        return '0'
        
all_funcs = locals()

# Test
if __name__ == "__main__":
    print all_funcs
    print '-----------------'
    
    print theme_path('home.html')
    print theme_path('/home.html')
    print theme_path('admin/home.html')

    print static_path('home.html')
    print static_path('/home.html', True)
    print static_path('admin/home.html')