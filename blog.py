# -*- coding: utf-8 -*-
from bottle import debug, Bottle, run, static_file, request, response, redirect, template
from setting import *
from utils import *
from model import *
from cache import cache_page

debug(is_debug)
app = Bottle()

###############################################################################
# 登录验证装饰 ###################################################################
###############################################################################
def authenticated(func):
    def _authenticated(*args, **kwargs):
        browser = request.headers.get('User-Agent')
        user_cookie = request.get_cookie('user', cookie_secret)
        user_right = md5_str(Option.get('username') + browser + Option.get('password'))

        if user_cookie <> user_right:
            redirect('/login')
        else: return func(*args, **kwargs)

    return _authenticated


###############################################################################
# blog #########################################################################
###############################################################################

@app.get('/')
@authenticated
@cache_page('page_index_', lambda: get_param('paged', '1'))
def home():
    return render(thome, locals())


@app.get('/post/:postid')
@cache_page('page_post_', lambda postid: postid)
def post_detail(postid):
    return render(tpost, locals())


@app.get('/page/:enname')
@cache_page('page_post_', lambda enname: enname)
def page_detail(enname):
    return render(tpage, locals())


@app.get('/tag/:tagid')
@cache_page('page_tag_', lambda tagid: tagid + '_' + get_param('paged', '1'))
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
@app.get('/login')
def for_login():
    return render(tadmin_login)


@app.post('/login')
def login():
    username = get_param('username')
    password = md5_str(get_param('password'))
    username_right = Option.get('username')
    password_right = Option.get('password')

    if username == username_right and password == password_right:
        browser = request.headers.get('User-Agent')
        user2cookie = md5_str(Option.get('username') + browser + Option.get('password'))
        response.set_cookie('user', user2cookie, cookie_secret)

    redirect('/admin')


@app.get('/admin')
@app.get('/admin/post-edit/:id')
@authenticated
def for_edit_post(id='0'):
    return 'admin'


###############################################################################
# other ########################################################################
###############################################################################

#------------------------------------------
@app.get('/static/:filename#.+#')
@app.get('/:filename#favicon.ico#')
def service_static_file(filename):
    return static_file(filename, root=template_dir)


# 参数
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


# Local Test
if __name__ == "__main__":
    run(app, port=8080, reloader=True)