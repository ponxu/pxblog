# -*- coding: utf-8 -*-
import json
from math import ceil
from tornado.web import RequestHandler
from func4temp import all_funcs
from utils import merge_dict, fmt_time
from setting import page_size, is_debug


def get_paged(handler):
    """ 页码 """
    return int(handler.get_argument('paged', '1'))


class BlogHandler(RequestHandler):
    """ 所有Handler基类 """

    if not is_debug:
        def write_error(self, status_code, **kwargs):
            self.write("您访问的资源可能已经不存在, <a href='/'>返回首页</a>")

    def get_current_user(self):
        # return self.get_secure_cookie("user")
        return 'test_user'

    def render_json(self, obj):
        self.write(json.dumps(obj))

    def render(self, template_name, root=None):
        # 添加方法到模板
        kwargs = merge_dict(root, all_funcs)
        # 移除self
        if kwargs.has_key('self'):
            del kwargs['self']
            # 生成html
        html = self.render_string(template_name, **kwargs)
        html += '<!-- generated when %s, use %fms -->' % (fmt_time(), self.request.request_time())

        self.write(html)
        return html


class PageInfo:
    """ 分页信息封装 """

    def __init__(self, paged, total, url, paged_size=page_size):
        self.paged = paged
        self.total = total
        self.url = url
        self.paged_size = paged_size
        self.pages = int(ceil(float(total) / float(paged_size)))
        self.pre = (paged > 1) and (paged - 1) or 1
        self.next = (paged < self.pages) and (paged + 1) or self.pages

        if '?' in url:
            self.paged_url = url + '&paged='
        else:
            self.paged_url = url + '?paged='

        self.pre_url = self.paged_url + str(self.pre)
        self.next_url = self.paged_url + str(self.next)