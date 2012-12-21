# -*- coding: utf-8 -*-
import sae.kvdb
from setting import *

#Memcache 是否可用
mc = None
try:
    import pylibmc

    mc = pylibmc.Client()
    mc.set('check_memcache_available', '1', 3600)
    print 'memcache is available!!'
except:
    mc = None
    print 'can not use memcache!!'

# 读取缓存
def get_cache(key):
    if not mc or not key: return None
    return mc.get(key)


# 缓存
def set_cache(key, value, time=cache_time):
    if not mc or not key: return
    mc.set(key, value, time)


# Test
if __name__ == "__main__":
    set_cache('a', 'abc')
    print get_cache('')
    print get_cache('a')