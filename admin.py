# -*- coding: utf-8 -*-
from tornado.web import authenticated
from webcommon import *
from model import *
from setting import *
from utils import *
from file import *
from cache import flush_cache

#===========================================================
class PostQuery(BlogHandler):
    @authenticated
    def get(self):
        paged = get_paged(self)
        status = self.get_argument('status', '')
        type = self.get_argument('type', '')

        url = '/admin/post-query?type=%s&status=%s' % (type, status)

        posts, total = Post.query(paged, type=type, status=status)
        page_info = PageInfo(paged, total, url)

        return self.render(tadmin_post_list, {
            'posts': posts,
            'page_info': page_info
        })


class PostEdit(BlogHandler):
    @authenticated
    def get(self, id='0'):
        if id == '0':
            post = ObjectLikeDict(tags=[])
        else:
            post = Post.get_by_id(int(id))
        return self.render(tadmin_post_edit, locals())

    @authenticated
    def post(self):
        post = ObjectLikeDict(
            id=int(self.get_argument('id', '0')),
            url=self.get_argument('url', ''),
            title=self.get_argument('title', ''),
            content=self.get_argument('content', ''),
            top=int(self.get_argument('top', '0')),
            status=self.get_argument('status', 'publish'),
            type=self.get_argument('type', 'post'),
            password=self.get_argument('password', ''),
        )

        tagids = [int(i) for i in self.get_arguments('tagid')]

        if post.id == 0:
            id = Post.add(post, tagids)
        else:
            Post.modify(post, tagids)
            id = post.id

        self.render_json(id)
        flush_cache()


class PostDelete(BlogHandler):
    @authenticated
    def get(self, id):
        self.render_json(Post.remove(int(id)))
        flush_cache()

#===========================================================
class TagEdit(BlogHandler):
    @authenticated
    def get(self):
        tags = Tag.all()
        return self.render(tadmin_tag, locals())

    @authenticated
    def post(self):
        tag = ObjectLikeDict(
            id=int(self.get_argument('id', '0')),
            name=self.get_argument('name'),
            sort=int(self.get_argument('sort', '0')),
        )

        if tag.id == 0:
            id = Tag.add(tag.name)
        else:
            Tag.modify(tag)
            id = tag.id

        self.render_json(id)
        flush_cache()


class TagDelete(BlogHandler):
    @authenticated
    def get(self, id):
        self.render_json(Tag.remove(int(id)))
        flush_cache()

#===========================================================
class OptionEdit(BlogHandler):
    @authenticated
    def get(self):
        options = Option.all()
        return self.render(tadmin_option, locals())

    @authenticated
    def post(self):
        id = int(self.get_argument('id', '0'))
        name = self.get_argument('name', '')
        value = self.get_argument('value', '')
        description = self.get_argument('description', '')

        if name == 'password':
            old = Option.get('password')
            if value <> old:
                value = md5(value)

        if id == 0:
            id = Option.set(name, value, description)
        else:
            Option.set(name, value)

        self.render_json(id)
        flush_cache()

#===========================================================
class LinkEdit(BlogHandler):
    @authenticated
    def get(self):
        links = Link.query()
        return self.render(tadmin_link, locals())

    @authenticated
    def post(self):
        link = ObjectLikeDict(
            id=int(self.get_argument('id', '0')),
            name=self.get_argument('name', ''),
            sort=int(self.get_argument('sort', '0')),
            description=self.get_argument('description', ''),
            url=self.get_argument('url', ''),
            icon=self.get_argument('icon', ''),
            status=self.get_argument('status', 'hidden'),
        )

        if link.id == 0:
            id = Link.add(link)
        else:
            Link.modify(link)
            id = link.id

        self.render_json(id)
        flush_cache()


class LinkDelete(BlogHandler):
    @authenticated
    def get(self, id):
        self.render_json(Link.remove(int(id)))
        flush_cache()

#===========================================================
class FileManage(BlogHandler):
    def get(self, filename):
        self.write(read(filename))

    @authenticated
    def post(self):
        file = self.request.files['filedata'][0]
        saved_file_name = "%d%s" % (now(), file['filename'])
        data = file['body']
        url = save(saved_file_name, data)
        self.write(url)

#===========================================================
class Login(BlogHandler):
    def _check_login(self):
        cookie_user = self.get_secure_cookie('user')
        right_user = md5(Option.get('username') + Option.get('password'))
        return cookie_user == right_user

    def get(self):
        if self._check_login():
            self.redirect('/admin')
        else:
            self.render(tadmin_login)

    def post(self):
        username = self.get_argument('username', '')
        password = md5(self.get_argument('password', ''))

        if Option.get('username') == username and Option.get('password') == password:
            # 登录成功: 保存登录信, 跳到发布文章页面
            user = md5(username + password)
            self.set_secure_cookie('user', user, cookie_timeout)
            self.redirect('/admin')
        else:
            # 登录失败: 跳到登录页面
            self.redirect(self.get_login_url())


class Logout(BlogHandler):
    def get(self):
        self.clear_cookie('user')
        self.redirect('/')