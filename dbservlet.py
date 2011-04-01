import sqlite3, hashlib, time

from utilsservlet import rand_alpha_numeric

try:
    conn = sqlite3.connect('pfsdb')
except OperationalError:
    from utilsservlet import create_db
    create_db
    conn = sqlite3.connect('pfsdb')

class db:
    @staticmethod
    def query_filekey(key, con=conn):
        cursor = con.cursor()
        query = (key,)
        cursor.execute('select * from files where key=?', query)
        return cursor.fetchone()[1]
    @staticmethod
    def query_files_user(user):
        cursor = conn.cursor()
        query = (user,)
        cursor.execute('select * from files where user=?', query)
        return cursor.fetchall()
    @staticmethod
    def insert_file(filepath, user, con=conn):
        key=rand_alpha_numeric(14)
        date=time.asctime(time.gmtime())
        try:
            cursor = con.cursor()
            query = (key, filepath, user, date,)
            cursor.execute('insert into files(key, path, user, time) values (?,?,?,?)', query)
            con.commit()
        except:
            return None
        return key
    @staticmethod
    def query_user(user, passwd, con=conn):
        user_pass_hash = hashlib.md5()
        user_pass_hash.update(user+passwd)
        cursor = con.cursor()
        query = (user_pass_hash.hexdigest(),)
        cursor.execute('select * from users where hash=?', query)
        return cursor.fetchone()
    @staticmethod
    def add_user(user, passwd, email, premium='', verified=False):
        conn = sqlite3.connect('pfsdb')
        user_pass_hash = hashlib.md5()
        user_pass_hash.update(user+passwd)
        key = user_pass_hash.hexdigest()
        date=time.asctime(time.gmtime())
        #try:
        cursor = conn.cursor()
        query = (key, user, email, time.asctime(time.gmtime()), verified, premium)
        cursor.execute('insert into users(hash,name,email,datejoined,verified,premium) values (?,?,?,?,?,?)', query)
        conn.commit()
        #except:
        #    return None
        return key