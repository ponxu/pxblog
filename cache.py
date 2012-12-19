# -*- coding: utf-8 -*-
import sae.kvdb
from setting import *

# TODO use memcache

kv = sae.kvdb.KVClient()
# 读取缓存
def get_cache(key):
    if not key: return ''
    print key
    return kv.get(key)


# 缓存
def set_cache(key, value, time=cache_time):
    if not key: return
    kv.add(key, value, time)


# Test
if __name__ == "__main__":
    set_cache('a', 'abc')
    print get_cache('')
    print get_cache('a')