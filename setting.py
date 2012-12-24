# -*- coding: utf-8 -*-
import os

# === user =========================
theme = 'simple'
page_size = 15
cookie_secret = '*&HGF%Ksdf*@1sdf~~~``&8+))___+^^'

# ===system=========================
is_debug = True
template_dir = 'templates'
theme_admin = 'admin'
is_cache_page = True
cache_time = 24 * 3600 # sec

# --- 模板名字 --------
thome = 'home.html'
tlist = 'list.html'
tpost = 'post.html'
tpage = 'page.html'

tadmin_post_edit = '%s/post-edit.html' % theme_admin
tadmin_post_list = '%s/post-list.html' % theme_admin
tadmin_setting = '%s/setting.html' % theme_admin
tadmin_tag = '%s/tag.html' % theme_admin
tadmin_login = '%s/login.html' % theme_admin

is_local = 'SERVER_SOFTWARE' not in os.environ
is_sae = 'SERVER_SOFTWARE' in os.environ

db_host = '127.0.0.1'
db_port = 3306
db_user = 'root'
db_passwd = 'root'
db_name = 'pxblog'

db_host2 = '127.0.0.1'
db_port2 = 3306
db_user2 = 'root'
db_passwd2 = 'root'
db_name2 = 'pxblog'

# 数据库连接超时(秒)
max_idle_time = 10

if is_sae:
    import sae.const

    db_host = sae.const.MYSQL_HOST
    db_host2 = sae.const.MYSQL_HOST_S

    db_port = db_port2 = int(sae.const.MYSQL_PORT)
    db_name = db_name2 = sae.const.MYSQL_DB
    db_user = db_user2 = sae.const.MYSQL_USER
    db_passwd = db_passwd2 = sae.const.MYSQL_PASS


# Test
if __name__ == "__main__":
    print is_sae