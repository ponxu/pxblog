# -*- coding: utf-8 -*-
import os
import tornado.wsgi
import tornado.web
import sae

from blog import *
from admin import *

settings = {
    'debug': True,
    'static_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'cookie_secret': 'hello_secret',
    'login_url': '/login',
    #'xsrf_cookies': True,
    'gzip': True,
    'autoescape': None,
}

handlers = [
    (r'/static/(.+)', tornado.web.StaticFileHandler, dict(path=settings['static_path'])),
    (r'/(favicon\.ico)', tornado.web.StaticFileHandler, dict(path=settings['static_path'])),

    # -- blog ----------------------
    (r'/', Home),
    (r'/post/(\d+)', PostDetail),
    (r'/note/(\d+)', PostDetail),
    (r'/page/(.+)', PageDetail),
    (r'/tag/(\d+)', SearchByTag),
    (r'/search', Search),

    # -- admin ---------------------
    (r'/login', Login),
    (r'/logout', Logout),

    (r'/admin', PostEdit), # 登录首页
    (r'/admin/post-query', PostQuery),
    (r'/admin/post-edit', PostEdit),
    (r'/admin/post-edit/(\d+)', PostEdit),
    (r'/admin/post-del/(\d+)', PostDelete),

    (r'/admin/tag-edit', TagEdit),
    (r'/admin/tag-del/(\d+)', TagDelete),
    (r'/admin/link-edit', LinkEdit),
    (r'/admin/link-del/(\d+)', LinkDelete),
    (r'/admin/option', OptionEdit),

    #-- 附件 --
    (r'/admin/upload', FileManage),
    (r'/attachment/(.+)', FileManage),

    # -- SEO ---------------------
    (r"/robots\.txt", Robots),
    (r"/sitemap\.xml", Sitemap),
    (r"/rss", RSS),
]

tornado_app = tornado.wsgi.WSGIApplication(**settings)
tornado_app.add_handlers(r'.*', handlers)

application = sae.create_wsgi_app(tornado_app)

if __name__ == '__main__':
    import wsgiref.simple_server

    server = wsgiref.simple_server.make_server('', 8080, tornado_app)
    server.serve_forever()