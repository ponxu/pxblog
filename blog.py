# -*- coding: utf-8 -*-
from webcommon import *
from cache import cache_page
from setting import *
from model import *


class Home(BlogHandler):
    @cache_page('page_home_', get_paged)
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


class SearchByTag(BlogHandler):
    @cache_page('page_tag_', lambda handler, tagid: '%s_%d' % (tagid, get_paged(handler)))
    def get(self, tagid):
        paged = get_paged(self)
        url = '/tag/' + tagid
        posts, total = Post.query(paged, type='post', status='publish', tagid=tagid)
        page_info = PageInfo(paged, total, url)
        return self.render(tlist, locals())


class Search(BlogHandler):
    def get(self):
        s = self.get_argument('s', '')
        paged = get_paged(self)
        url = '/search?s=%s' % s
        posts, total = Post.query(paged, type='post', status='publish', keywords=s)
        page_info = PageInfo(paged, total, url)
        return self.render(tlist, locals())

#=====================================================================

class Robots(BlogHandler):
    @cache_page('page_robots')
    def get(self):
        return self.render(tseo_robots)

    def request_time_info(self):
        return ''


class Sitemap(BlogHandler):
    @cache_page('page_sitemap')
    def get(self):
        self.set_header('Content-Type', 'text/xml')
        return self.render(tseo_sitemap)


class RSS(BlogHandler):
    @cache_page('page_rss')
    def get(self):
        self.set_header('Content-Type', 'text/xml')
        return self.render(tseo_rss)