# -*- coding: utf-8 -*-
from hashlib import md5

# 字典,像对象一样访问
class ObjectLikeDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except:
            return ""

# 合并字典
def merge_dict(dict1, dict2):
    return (lambda a, b: (lambda a_copy: a_copy.update(b) or a_copy)(a.copy()))(dict1, dict2)

# 转数组
def to_list(obj):
    if isinstance(obj, list): return obj
    else: return [obj]

# 当前时间
def now_str(fmt='%Y-%m-%d %H:%M:%S'):
    return ''


# 字符串MD5值
def md5_str(s):
    m = md5()
    m.update(s)
    return m.hexdigest()

# Test
if __name__ == "__main__":
    t = ObjectLikeDict()
    t['test'] = 'i am a test'
    print 'test=%s' % t.test
    print '---------------------'

    dict1 = {'a': 1, 'b': 2}
    dict2 = {'c': 3, 'd': 4}
    print merge_dict(dict1, dict2)

    print md5_str('')