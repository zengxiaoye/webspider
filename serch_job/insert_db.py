# coding=utf-8

try:
    import MySQLdb as mysqldb
    from MySQLdb import InternalError
except ImportError:
    import pymysql as mysqldb
    from pymysql.err import InternalError

conn_instance_dict = {}

DB_CONFIG = {
    # 'host':'IP', 'port' : 3306, 'user':'自己密码', 'passwd':'666',
    'host': 'localhost', 'port': 3306, 'user': 'root', 'passwd': 'root',
    'charset': 'utf8',
    'db': 'test',
}


def _newConn(db):
    DB_CONFIG.update(db=db)
    conn = mysqldb.connect(**DB_CONFIG)
    return conn

def getConn(db):
    try:
        conn = conn_instance_dict[db]
        conn.ping()
        return conn
    except (InternalError, KeyError):
        conn = _newConn(db)
        conn_instance_dict[db] = conn
        return conn

def insertDB(data, db, table):
    if not data:
        return
    try:
        conn = getConn(db)
    except BaseException as e:
        print (e)
    cur = conn.cursor()
    if isinstance(data, tuple):
        params = ','.join(['%s'] * len(data))
        sql = 'insert into %s()' \
              'values(%s) ' % (table, params)
        cur.execute(sql, data)
    else:
        params = ','.join(['%s'] * len(data[0]))
        sql = 'insert into %s()'\
              'values(%s) ' % (table, params)
        try:
            cur.executemany(sql, data)
        except Exception as e:
            print (e)
            print (sql)
    cur.close()
    conn.commit()


