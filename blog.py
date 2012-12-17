# -*- coding: utf-8 -*-
import os
from bottle import debug, Bottle, run, static_file, request
from setting import *

debug(is_debug)
app = Bottle()

###############################################################################
# 页面缓存 #####################################################################
###############################################################################
from cache import *

def cache(key_prefix="", key_suffix_func=None, time=cache_time):
    def _cache(func):
        def __cache(*args, **kwargs):
            real_key = key_prefix
            if key_suffix_func:
                key_suffix = key_suffix_func(*args, **kwargs)
                real_key += key_suffix
            content = get_cache(real_key)
            if content:
                return content
            else:
                content = func(*args, **kwargs)
                set_cache(real_key, content, time)
                return content
        return __cache
    return _cache

###############################################################################
# blog #########################################################################
###############################################################################

@app.get('/')
@cache('index_', lambda: request.GET.get('page', '1'))
def index():
    print 'index............'
    return render('test.html', name='xwz' + request.GET.get('page', '1'))
    

###############################################################################
# admin ########################################################################
###############################################################################



@app.get('/static/:filename#.+#')
@app.get('/:filename#favicon.ico#')
def service_static_file(filename):
    print 'static file: %s' % filename
    return static_file(filename, root=template_dir)
    
    
###############################################################################
# 模板 #########################################################################
###############################################################################
from jinja2 import Environment, FileSystemLoader
from func4temp import theme_path

env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), template_dir)))

def render(template_name, *args, **kwargs):
    t = env.get_template(theme_path(template_name))
    return t.render(*args, **kwargs)
    
    
if __name__ == "__main__":
    run(app, port=8080, reloader=True)