# -*- coding: utf-8 -*-
import sae.kvdb
from setting import *

# TODO use memcache
# 读取缓存
def get_cache(key):
    kv = sae.kvdb.KVClient()
    value = kv.get(key)
    print '%s=%s' % (key, value)

    return value

# 缓存
def set_cache(key, value, time):
    kv = sae.kvdb.KVClient()
    kv.add(key, value, time)

# 缓存页面
def pagecache(key_prefix="", key_suffix_func=None, time=cache_time):
    def _cache(func):
        def __cache(*args, **kwargs):
            real_key = key_prefix
            if key_suffix_func:
                key_suffix = key_suffix_func(*args, **kwargs)
                real_key += key_suffix

            content = get_cache(real_key)
            if content:
                return content
            else:
                content = func(*args, **kwargs)
                set_cache(real_key, content, time)
                return content

        return __cache

    return _cache