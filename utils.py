# -*- coding: utf-8 -*-
import hashlib
import time
from datetime import datetime, timedelta

# 字典,像对象一样访问
class ObjectLikeDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except:
            return ""

# 合并字典
def merge_dict(dict1, dict2):
    return (lambda a, b: (lambda a_copy: a_copy.update(b) or a_copy)(a.copy()))(dict1 or {}, dict2 or {})

# 转数组
def to_list(obj):
    if isinstance(obj, list): return obj
    else: return [obj]

# 格式化时间, 默认返回当前时间
def fmt_time(fmt='%Y-%m-%d %H:%M:%S', seconds=None):
    if not seconds: seconds = now()
    t = datetime.utcfromtimestamp(seconds)
    t = t + timedelta(hours=+8) # 时区
    return t.strftime(fmt)

# 当前时间戳(精确到秒)
def now():
    return int(time.time())


# 字符串MD5值
def md5(s):
    m = hashlib.md5(s)
    m.digest()
    return m.hexdigest()

def unicode2str(ustr):
    if isinstance(ustr, unicode):
        return ustr.encode('utf8')
    return ustr

# Test
if __name__ == "__main__":
    dict1 = {'a': 1, 'b': 2}
    dict2 = {'c': 3, 'd': 4}
    print merge_dict(dict1, dict2)

    print md5('')

    print now()
    print fmt_time()