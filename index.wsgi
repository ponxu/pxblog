import os
import tornado.wsgi
import sae

from blog import *

settings = {
    'debug': True,
    'static_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'template_path': os.path.join(os.path.dirname(__file__), 'templates'),
    'cookie_secret': 'hello_secret',
    'login_url': '/login',
    'xsrf_cookies': True,
    'gzip': True,
    'autoescape': None,
}

handlers = [
    (r'/test', TestHandler),
    (r'/', Home),
]

app = tornado.wsgi.WSGIApplication(handlers, **settings)

application = sae.create_wsgi_app(app)

if __name__ == '__main__':
    import wsgiref.simple_server

    server = wsgiref.simple_server.make_server('', 8888, app)
    server.serve_forever()