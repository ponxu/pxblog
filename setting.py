# -*- coding: utf-8 -*-
import os

# === user =========================
# 主题
theme = 'simple'
# 分页大小
page_size = 5
# 登录cookie超时(天)
cookie_timeout = 7
# 是否开启页面缓存
is_cache_page = True

# ===system(一般情况不需要修改)=========================
is_debug = True
# 模板文件夹
template_dir = 'templates'
# 后台模板文件夹
theme_admin = 'admin'
# 默认momcache缓存时间
cache_time = 24 * 3600 # sec
# 文章摘要截取长度
sublength = 250
# SAE存储domain name
storage_domain = 'attachment'

# --- 模板名字 --------
thome = '%s/home.html' % theme
tlist = '%s/list.html' % theme
tpost = '%s/post.html' % theme
tpage = '%s/page.html' % theme

tadmin_post_edit = '%s/post-edit.html' % theme_admin
tadmin_post_list = '%s/post-list.html' % theme_admin
tadmin_option = '%s/option.html' % theme_admin
tadmin_tag = '%s/tag.html' % theme_admin
tadmin_login = '%s/login.html' % theme_admin
tadmin_link = '%s/link.html' % theme_admin

#----------------
is_local = 'SERVER_SOFTWARE' not in os.environ
is_sae = 'SERVER_SOFTWARE' in os.environ

#---数据库-------------
db_host = db_host2 =  '127.0.0.1'
db_port = db_port2 = 3306
db_user = db_user2 = 'root'
db_passwd = db_passwd2 = 'root'
db_name = db_name2 = 'pxblog'

# 数据库连接超时(秒)
max_idle_time = 10

#----------------

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