# -*- coding: utf-8 -*-
from setting import *

#Memcache
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


###############################################################################
# 页面缓存装饰 ###################################################################
###############################################################################
def cache_page(key_prefix, key_suffix_func=None, time=cache_time):
    def _cache(func):
        def __cache(*args, **kwargs):
            # 不进行页面缓存
            if not is_cache_page: return func(*args, **kwargs)

            real_key = key_prefix
            # 计算后缀
            if key_suffix_func:
                key_suffix = key_suffix_func(*args, **kwargs)
                real_key += key_suffix

            # 读取缓存
            content = get_cache(real_key)

            if content:
                return content
            else:
                # 生成, 并缓存起来
                content = func(*args, **kwargs)
                set_cache(real_key, content, time)
                return content

        return __cache

    return _cache

# Test
if __name__ == "__main__":
    set_cache('a', 'abc')
    print get_cache('')
    print get_cache('a')