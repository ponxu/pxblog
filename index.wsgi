import sae
import web

application = sae.create_wsgi_app(web.app)