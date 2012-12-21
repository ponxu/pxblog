# -*- coding: utf-8 -*-
import torndb as database
from setting import *

mdb = sdb = database.Connection(db_host, db_name, db_user, db_passwd, max_idle_time)
if is_sae: sdb = database.Connection(db_host2, db_name2, db_user2, db_passwd2, max_idle_time)

class _Post:
    def query(self, page, page_size, type='post', keywords=None, tagid=None, status=None):
        ''' 综合查询 '''
        sql = "select * from px_post"
        count_sql = "select count(*) from px_post"

        condition = ""
        if type:
            condition += " and type='%s'" % type
        if status:
            if not isinstance(status, list):
                status = [status]
            condition += " and status in ('%s')" % "','".join(status)
        if keywords:
            like = ""
            for kw in keywords.split(' '):
                if kw:
                    like += " or title like '%%%%%s%%%%'" % kw
                    like += " or content like '%%%%%s%%%%'" % kw
            if like:
                condition += " and (" + like[4:] + ")"
        if tagid:
            if not isinstance(tagid, list):
                tagid = [tagid]
            condition += (" and exists (select tag_id from px_post_tag pt where px_post.id=pt.post_id and tag_id in (%s))"
                          % ",".join([str(d) for d in tagid]))

        if condition:
            sql += ' where ' + condition[5:]
            count_sql += ' where ' + condition[5:]

        sql += ' order by top desc, id asc limit %d,%d' % ((page - 1) * page_size, page_size)

        print sql
        print count_sql

        return sdb.query(sql), sdb.get(count_sql)['count(*)']

    def add(self, post):
        pass

Post = _Post()

def create_init_table():
    sql = '''
    '''
    mdb.execute(sql)

# Test
if __name__ == "__main__":
    tagid = 1
    type='page'
    keywords='1 2 3 4'
    status= 'password'
    print Post.query(1, 100, type=type, keywords=keywords, tagid=tagid, status=status)