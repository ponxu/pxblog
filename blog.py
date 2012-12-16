# -*- coding: utf-8 -*-
import os
from bottle import debug, Bottle, run, static_file, request
from setting import *
from cache import pagecache

debug(is_debug)
app = Bottle()

@app.get('/')
@pagecache('index_', lambda: request.GET.get('page', '1'))
def index():
    print 'index............'
    return render('test.html', name='xwz' + request.GET.get('page', '1'))


@app.get('/static/:filename#.+#')
@app.get('/:filename#favicon.ico#')
def service_static_file(filename):
    print 'static file: %s' % filename
    return static_file(filename, root=template_dir)

# 模板
from jinja2 import Environment, FileSystemLoader

env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), template_dir)))

def render(template_name, *args, **kwargs):
    t = env.get_template('themes/' + theme + '/' + template_name)
    return t.render(*args, **kwargs)

if __name__ == "__main__":
    run(app, port=8080, reloader=True)