# -*- coding: utf-8 -*-
import tenjin
#tenjin.set_template_encoding('utf-8')  # optional (defualt 'utf-8')
from tenjin.helpers import *
from tenjin.html import *
#import tenjin.gae; tenjin.gae.init()   # for Google App Engine
engine = tenjin.Engine()
context = { 'items': ['<AAA>', 'B&B', '"CCC"'] }
html = engine.render('example.pyhtml', context)
print(html)