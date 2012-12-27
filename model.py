# -*- coding: utf-8 -*-
from tornado import database
from setting import *
from utils import *

mdb = sdb = database.Connection(db_host, db_name, db_user, db_passwd, max_idle_time)
if is_sae: sdb = database.Connection(db_host2, db_name2, db_user2, db_passwd2, max_idle_time)

__all__ = ('Post', 'Tag', 'Option', 'Link')

class _Option:
    def get(self, name):
        row = sdb.get('select value from px_option where name=%s', name)
        if row:
            return row.value
        else:
            return None

    def set(self, name, value, description=''):
        old = self.get(name)
        if old is not None:
            sql = 'update px_option set value=%s where name=%s'
            return mdb.execute_rowcount(sql, value, name)
        else:
            sql = 'insert into px_option(name,value,description) values(%s,%s,%s)'
            return mdb.execute_lastrowid(sql, name, value, description)

    def all(self):
        return sdb.query('select * from px_option order by id asc, name asc')

Option = _Option()

class _Tag:
    def get_by_id(self, id):
        return sdb.get('select * from px_tag where id=%s', id)

    def all(self):
        return sdb.query('select * from px_tag order by sort desc, id asc')

    def add(self, name):
        return mdb.execute_lastrowid('insert into px_tag(name) values(%s)', name)

    def remove(self, id):
        mdb.execute_rowcount('delete from px_post_tag where tag_id=%s', id)
        return mdb.execute_rowcount('delete from px_tag where id=%s', id)

    def modify(self, tag):
        sql = 'update px_tag set name=%s,sort=%s where id=%s'
        return mdb.execute_rowcount(sql, tag.name, tag.sort, tag.id)

Tag = _Tag()

class _Link:
    def query(self, status=None):
        sql = 'select * form px_link'
        if status:
            sql += " where status='%s'" % status
        sql += ' order by sort desc, id asc'
        return sdb.query(sql)

    def add(self, link):
        sql = '''insert into px_link(name,url,description,
            icon,status,sort) values(%s,%s,%s,%s,%s,%s)'''
        return mdb.execute_lastrowid(sql,
            link.name,
            link.url,
            link.description,
            link.icon,
            link.status,
            link.sort)

    def modify(self, link):
        sql = '''update px_link set name=%s,url=%s,
            description=%s,icon=%s,status=%s,sort=%s
            where id=%s'''
        return mdb.execute_rowcount(sql,
            link.name,
            link.url,
            link.description,
            link.icon,
            link.status,
            link.sort,
            link.id)

    def remove(self, id):
        return mdb.execute_rowcount('delete from px_link where id=%s', id)

Link = _Link()

class _Post:
    def get_by_id(self, id):
        return self._set_tag(sdb.get('select * from px_post where id=%s', id))

    def get_by_url(self, url):
        return self._set_tag(sdb.get('select * from px_post where url=%s', url))

    def add(self, post, tagids):
        sql = '''insert into px_post(
            url,title,content,addtime,top,
            status,type,password)
            values(%s,%s,%s,%s,%s,%s,%s,%s)'''
        id = mdb.execute_lastrowid(sql,
            post.url,
            post.title,
            post.content,
            now(),
            post.top,
            post.status,
            post.type,
            post.password)
        for tagid in tagids:
            self._add_tag(id, tagid)
        return id

    def modify(self, post, new_tagids):
        self._set_tag(post)

        old_tagids = [tag.id for tag in post.tags]

        # 移除删除的标签
        for tagid in old_tagids:
            if tagid not in new_tagids:
                old_tagids.remove(tagid)
                #post.tags.remove(???)
                self._remove_tag(post.id, tagid)

        # 增加新选择标签
        for tagid in new_tagids:
            if tagid not in old_tagids:
                self._add_tag(post.id, tagid)

        # 更新
        sql = '''update px_post set
            url=%s,title=%s,content=%s,top=%s,
            status=%s,type=%s,password=%s
            where id=%s'''
        return mdb.execute_rowcount(sql,
            post.url,
            post.title,
            post.content,
            post.top,
            post.status,
            post.type,
            post.password,
            post.id)

    def remove(self, id):
        mdb.execute_rowcount('''
            update px_tag set post_count=post_count-1
            where post_count>0 and exists (
                select tag_id from px_post_tag pt
                where px_tag.id=pt.tag_id and pt.post_id=%s
            )''', id)
        mdb.execute_rowcount('delete from px_post_tag where post_id=%s', id)
        return mdb.execute_rowcount('delete from px_post where id=%s', id)

    def query(self, paged,
              paged_size=page_size,
              type=None,
              status=None,
              keywords=None,
              tagid=None,
              other_condition=None,
              order='top desc, id desc'):
        """ 综合查询 """
        sql = 'select id,url,title,left(content, %d) as content,addtime,top,status,type,password from px_post' % sublength
        count_sql = 'select count(*) from px_post'

        #----where------------------------------------------------------
        condition = ''
        # 类型
        if type:
            condition += " and type='%s'" % type

        # 状态
        if status:
            condition += " and status in ('%s')" % "','".join(to_list(status))

        # 关键字
        if keywords:
            like = ""
            for kw in keywords.split(' '):
                if kw:
                    like += " or title like '%%%%%s%%%%'" % kw
                    like += " or content like '%%%%%s%%%%'" % kw
            if like:
                condition += ' and (' + like[4:] + ')'

        # 标签
        if tagid:
            condition += (
                ' and exists (select tag_id from px_post_tag pt where px_post.id=pt.post_id and tag_id in (%s))'
                % ','.join([str(d) for d in to_list(tagid)]))

        # 其他条件
        if other_condition:
            condition += ' and %s' % other_condition

        # where
        if condition:
            sql += ' where ' + condition[5:]
            count_sql += ' where ' + condition[5:]

        #----------------------------------------------------------

        # 排序
        if order:
            sql += ' order by %s' % order

        # 分页
        sql += ' limit %d,%d' % ((paged - 1) * paged_size, paged_size)

        print sql

        return self._set_tag(sdb.query(sql)), sdb.get(count_sql)['count(*)']

    def _set_tag(self, posts):
        """ 给文章设置标签信息 """
        if posts is None:
            return None

        post_array = to_list(posts)

        # 查询文章和标签关联关系
        postids = [post.id for post in post_array]
        relation = self._get_relation(postids)

        # 关联
        for post in post_array:
            post.tags = filter(lambda tag: self._has_relation(post.id, tag.id, relation), Tag.all())

        return posts

    def _has_relation(self, postid, tagid, relation):
        """ 文章和标签是否有关系 """
        if postid and tagid and relation:
            for r in relation:
                if r.post_id == postid and r.tag_id == tagid:
                    return True
        return False

    def _get_relation(self, postids):
        """ 获取文章和标签的关系 """
        in_ids = ','.join([str(i) for i in to_list(postids)])
        if in_ids:
            return sdb.query('select * from px_post_tag where post_id in (%s)' % in_ids)
        else:
            return []

    def _add_tag(self, postid, tagid):
        """ 给文章添加一个标签 """
        mdb.execute_rowcount('insert into px_post_tag values(%s,%s)', postid, tagid)
        mdb.execute_rowcount('update px_tag set post_count=post_count+1 where id=%s', tagid)

    def _remove_tag(self, postid, tagid):
        """ 移除文章的一个标签 """
        mdb.execute_rowcount('delete from px_post_tag where post_id=%s and tag_id=%s', postid, tagid)
        mdb.execute_rowcount('update px_tag set post_count=post_count-1 where post_count>0 and id=%s', tagid)

Post = _Post()

def create_init_table():
    sql = '''
    '''
    mdb.execute(sql)

# Test
if __name__ == "__main__":
    print Post.query(1)

