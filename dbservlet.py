import sqlite3, hashlib

conn = sqlite3.connect('fs.db')
conn.connect()

class db:   
    @staticmethod
    def query_filekey(key):
        cursor = conn.cursor()
        query = (key,)
        cursor.execute('select * from files where key=?', query)
        return cursor[1]
    @staticmethod
    def query_user(user, passwd):
        user_pass_hash = hashlib.md5()
        user_pass_hash.update(user+passwd)
        cursor = conn.cursor()
        query = (user_pass_hash.hexdigest(),)
        cursor.execute('select * from files where key=?', query)
        return cursor