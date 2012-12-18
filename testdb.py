# -*- coding: utf-8 -*-
import MySQLdb
from MySQLdb.cursors import DictCursor
from setting import *

class Row:
    def __init__(self, dct):
        self.data = dct

    def __str__(self):
        return str(self.data)

    def __getattr__(self, name):
        try:
            return self.data[name]
        except:
            return ""


class RowList:
    def __init__(self, dict_list):
        self.data = dict_list

    def __str__(self):
        return str(self.data)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, i):
        return Row(self.data[i])


def execute(sql, value=None):
    conn = MySQLdb.connect(host=db_host, port=db_port, db=db_name, user=db_user, passwd=db_user, charset='utf8')
    cursor = conn.cursor()
    n = cursor.execute(sql, value)
    conn.commit()
    cursor.close()
    conn.close()
    return n


def query(sql, value=None):
    conn = MySQLdb.connect(host=db_host2, port=db_port2, db=db_name2, user=db_user2, passwd=db_user2, charset='utf8')
    cursor = conn.cursor(DictCursor)
    n = cursor.execute(sql, value)
    print n
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return RowList(rows)


def queryone(sql, value=None):
    conn = MySQLdb.connect(host=db_host2, port=db_port2, db=db_name2, user=db_user2, passwd=db_user2, charset='utf8')
    cursor = conn.cursor(DictCursor)
    n = cursor.execute(sql, value)
    print n
    row = cursor.fetchone()
    cursor.close()
    conn.close()
    return Row(row)


# table
# execute('create table test(id int, info varchar(100))')

# insert
print execute("insert into test values(11,'test')")
print '----------------------------------------'

# query
print queryone('select * from test').id
print '----------------------------------------'

for row in query('select * from test'):
    print row