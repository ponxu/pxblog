# -*- coding: utf-8 -*-
import json
from tornado.web import RequestHandler
from func4temp import all_funcs
from utils import *

def get_paged(handler):
    """ 页码 """
    return handler.get_argument('paged', '1')

class BlogHandler(RequestHandler):
    """ 所有Handler基类 """

    def write_error(self, status_code, **kwargs):
        self.write("您访问的资源可能已经不存在, <a href='/'>返回首页</a>")

    def get_current_user(self):
        return self.get_secure_cookie("user")

    def write_json(self, obj):
        self.write(json.dumps(obj))

    def check_login(self):
        return self.get_current_user()

    def render(self, template_name, root=None):
        # 添加方法到模板
        kwargs = merge_dict(root, all_funcs)
        # 移除self
        if kwargs.has_key('self'):
            del kwargs['self']
        # 生成html
        html = self.render_string(template_name, **kwargs)
        html += '<!-- generated when %s -->' % fmt_time()

        import time
        print time.clock()

        self.write(html)
        return html


class PageInfo:
    """ 分页信息封装 """

    def __init__(self, currentPage, url, total):
        self.url = url
        self.total = total
        self.currentPage = 0
        self.totalPage = 0
        self.prePage = 0
        self.nextPage = 0