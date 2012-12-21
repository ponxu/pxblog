# -*- coding: utf-8 -*-
import torndb as database
from setting import *

mdb = sdb = database.Connection(db_host, db_name, db_user, db_passwd, max_idle_time)
if is_sae: sdb = database.Connection(db_host2, db_name2, db_user2, db_passwd2, max_idle_time)

class _Post:
    def query(self):
        sql = 'select * from px_post'
        return None

    def add(self, post):
        pass

Post = _Post()

def create_init_table():
    sql = '''
    '''
    mdb.execute(sql)

# Test
if __name__ == "__main__":
    print mdb
    print sdb
    print Post