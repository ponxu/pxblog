# -*- coding: utf-8 -*-
import os
from bottle import debug, Bottle, run, static_file, request
from setting import *
from utils import *

debug(is_debug)
app = Bottle()

###############################################################################
# 页面缓存 #####################################################################
###############################################################################
from cache import *

def cache(key_prefix, key_suffix_func=None, time=cache_time):
    def _cache(func):
        def __cache(*args, **kwargs):
            real_key = key_prefix
            # 计算后缀
            if key_suffix_func:
                key_suffix = key_suffix_func(*args, **kwargs)
                real_key += key_suffix

            # 读取缓存
            content = get_cache(real_key)

            if content:
                return content
            else:
                # 生成, 并缓存起来
                content = func(*args, **kwargs)
                set_cache(real_key, content, time)
                return content

        return __cache

    return _cache


###############################################################################
# blog #########################################################################
###############################################################################

@app.get('/')
@cache('page_index_', lambda: get_param('paged', '1'))
def home():
    return render(temp_home, locals())


@app.get('/post/:postid')
@cache('page_post_', lambda postid: postid)
def post_detail(postid):
    return render(temp_post, locals())


@app.get('/page/:enname')
@cache('page_post_', lambda enname: enname)
def page_detail(enname):
    return render(temp_page, locals())


@app.get('/tag/:tagid')
@cache('page_tag_', lambda tagid: tagid + '_' + get_param('paged', '1'))
def posts_under_tag(tagid):
    return render(temp_list, locals())


@app.get('/search')
def search():
    s = get_param('s')
    print 's=%s' % s
    return render(temp_list, locals())


###############################################################################
# admin ########################################################################
###############################################################################


#------------------------------------------
@app.get('/static/:filename#.+#')
@app.get('/:filename#favicon.ico#')
def service_static_file(filename):
    print 'static file: %s' % filename
    return static_file(filename, root=template_dir)


def get_param(name, df=None):
    if 'GET' == request.method:
        return request.GET.get(name, df)
    elif 'POST' == request.method:
        return request.POST.get(name, df)
    else:
        return df


###############################################################################
# 模板 #########################################################################
###############################################################################
from jinja2 import Environment, FileSystemLoader
from func4temp import theme_path, all_funcs

env = Environment(loader=FileSystemLoader(os.path.join(os.path.dirname(__file__), template_dir)))

def render(template_name, *args, **kwargs):
    t = env.get_template(theme_path(template_name))
    new_kwargs = merge_dict(kwargs, all_funcs)
    return t.render(*args, **new_kwargs)


if __name__ == "__main__":
    run(app, port=8080, reloader=True)