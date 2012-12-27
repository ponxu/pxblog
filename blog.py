# -*- coding: utf-8 -*-
from webcommon import *
from cache import cache_page
from setting import *
from model import *


class Home(BlogHandler):
    @cache_page('page_index_', get_paged)
    def get(self):
        paged = get_paged(self)
        posts, total = Post.query(paged, type='post', status=['publish', 'password'])
        page_info = PageInfo(paged, total, '/')
        return self.render(thome, locals())


class PostDetail(BlogHandler):
    @cache_page('page_post_', lambda handler, id: id)
    def get(self, id):
        post = Post.get_by_id(int(id))
        return self.render(tpost, locals())


class PageDetail(BlogHandler):
    @cache_page('page_page_', lambda handler, url: url)
    def get(self, url):
        page = Post.get_by_url(url)
        return self.render(tpage, locals())