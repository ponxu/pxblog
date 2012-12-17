# -*- coding: utf-8 -*-
import sae.kvdb

# TODO use memcache
# 读取缓存
def get_cache(key):
    kv = sae.kvdb.KVClient()
    return kv.get(key)

# 缓存
def set_cache(key, value, time):
    kv = sae.kvdb.KVClient()
    kv.add(key, value, time)