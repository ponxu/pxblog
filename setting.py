# -*- coding: utf-8 -*-
import os

# === user =========================
theme = 'simple'
page_size = 15


# ===system=========================
is_debug = True
template_dir = 'templates'
theme_admin = 'admin'
cache_time = 365

# --- 模板名字 --------
temp_home = 'home.html'
temp_list = 'list.html'
temp_post = 'post.html'
temp_page = 'page.html'

temp_admin_post_edit = '%s/post-edit.html' % theme_admin
temp_admin_post_list = '%s/post-list.html' % theme_admin
temp_admin_setting = '%s/setting.html' % theme_admin
temp_admin_tag = '%s/tag.html' % theme_admin
temp_admin_login = '%s/login.html' % theme_admin

is_local = 'SERVER_SOFTWARE' not in os.environ
is_sae = 'SERVER_SOFTWARE' in os.environ

db_host = 'localhost'
db_port = 3306
db_user = 'root'
db_passwd = 'root'
db_name = 'pxblog'

db_host2 = 'localhost'
db_port2 = 3306
db_user2 = 'root'
db_passwd2 = 'root'
db_name2 = 'pxblog'

if is_sae:
    import sae.const
    db_host = sae.const.MYSQL_HOST
    db_port = int(sae.const.MYSQL_PORT)
    db_user = sae.const.MYSQL_USER
    db_passwd = sae.const.MYSQL_PASS
    db_name = sae.const.MYSQL_DB
    
    
# Test
if __name__ == "__main__":
    print is_sae