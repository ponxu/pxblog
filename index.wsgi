import sae
import blog

application = sae.create_wsgi_app(blog.app)