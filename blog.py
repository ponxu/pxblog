# -*- coding: utf-8 -*-
import os
from bottle import debug, Bottle, run, static_file, request
from setting import *
from utils import *
from model import *

debug(is_debug)
app = Bottle()

###############################################################################
# 页面缓存 #####################################################################
###############################################################################
from cache import *

def cache(key_prefix, key_suffix_func=None, time=cache_time):
    def _cache(func):
        def __cache(*args, **kwargs):
            # 不进行页面缓存
            if not is_cache_page: return func(*args, **kwargs)

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
    return render(thome, locals())


@app.get('/post/:postid')
@cache('page_post_', lambda postid: postid)
def post_detail(postid):
    return render(tpost, locals())


@app.get('/page/:enname')
@cache('page_post_', lambda enname: enname)
def page_detail(enname):
    return render(tpage, locals())


@app.get('/tag/:tagid')
@cache('page_tag_', lambda tagid: tagid + '_' + get_param('paged', '1'))
def posts_under_tag(tagid):
    return render(tlist, locals())


@app.get('/search')
def search():
    s = get_param('s')
    print 's=%s' % s
    return render(tlist, locals())


###############################################################################
# admin ########################################################################
###############################################################################


###############################################################################
# other ########################################################################
###############################################################################

#------------------------------------------
@app.get('/static/:filename#.+#')
@app.get('/:filename#favicon.ico#')
def service_static_file(filename):
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
from func4temp import theme_path, all_funcs
import tenjin
from tenjin.helpers import *

engine = tenjin.Engine(path=[template_dir], cache=False)

def render(template_name, *args, **kwargs):
    context = merge_dict(kwargs, all_funcs)
    return engine.render(theme_path(template_name), context)


if __name__ == "__main__":
    run(app, port=8080, reloader=True)