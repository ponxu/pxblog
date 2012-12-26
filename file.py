# -*- coding: utf-8 -*-
from setting import *

if is_sae:
    import sae.storage

    def save(name, data):
        s = sae.storage.Client()
        ob = sae.storage.Object(data)
        url = s.put(storage_domain, name, ob)
        return url


    def read(name):
        s = sae.storage.Client()
        ob = s.get(storage_domain, name)
        data = ob.data
        return data

else:
    def save(name, data):
        print 'save %s' % name
        return 'http://www.baidu.com/1.jpg'


    def read(name):
        print 'read %s' % name
        return None