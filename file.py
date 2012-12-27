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
    import os

    def _path(name):
        folder = os.path.join(os.path.dirname(__file__), 'attachment')
        if not os.path.exists(folder):
            os.makedirs(folder)
        return '%s/%s' % (folder, name)

    def save(name, data):
        f = None
        try:
            f = open(_path(name), 'wb')
            f.write(data)
        except:
            pass
        finally:
            if f: f.close()
        return '/attachment/' + name


    def read(name):
        f = None
        try:
            f = open(_path(name), 'rb')
            return f.read()
        except:
            pass
        finally:
            if f: f.close()

if __name__ == '__main__':
    print read('1.txt')
    print save('1.txt', '1111111111111111111111')