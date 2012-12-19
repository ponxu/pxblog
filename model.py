# -*- coding: utf-8 -*-

import torndb as database
from setting import *

mdb = database.Connection(db_host, db_name, db_user, db_passwd, max_idle_time)
sdb = database.Connection(db_host2, db_name2, db_user2, db_passwd2, max_idle_time)

# Test
if __name__ == "__main__":
    print mdb
    print sdb