# -*- coding: utf-8 -*-

class ObjectLikeDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except:
            return ""

# Test
if __name__ == "__main__":
    t = ObjectLikeDict()
    t['test'] = 'i am a test'
    print 'test=%s' % t.test