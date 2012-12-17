# -*- coding: utf-8 -*-

class NewDict(dict):
    def __getattr__(self, name):
        try:
            return self[name]
        except:
            return ""