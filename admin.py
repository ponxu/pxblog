# -*- coding: utf-8 -*-
from webcommon import *
from model import *
from setting import *

#===========================================================


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