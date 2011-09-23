import hashlib, time, sqlite3
try: import pymysql
except: pass
from utilsservlet import rand_alpha_numeric, settings

conn = None
db_type = settings['db_type']

def dbconnect():
    db_name=settings['db_name']
    if db_type == 'sqlite':
            try:
                 return sqlite3.connect(db_name)
            except sqlite3.OperationalError:
                 from utilsservlet import create_db
                 create_db(settings['db_name'])
                 return sqlite3.connect(db_name)
    elif db_type == 'mysql':
         try:
             return pymysql.connect(host=settings['db_host'], 
                                    port=settings['db_port'], 
                                    user=settings['db_username'], 
                                    passwd=settings['db_password'], 
                                    db=settings['db_name'])
         except pymysql.err.InternalError, e:
             print "MySQL internal error - ", e[0], ": ", e[1]
             pass

class db:
    @staticmethod
    def connect(db_name=settings['db_name']):
        if db_type == 'sqlite':
            try:
                 return sqlite3.connect(db_name)
            except OperationalError:
                 from utilsservlet import create_db
                 create_db(settings['db_name'])
                 return sqlite3.connect(db_name)
        elif db_type == 'mysql':
         try:
             return pymysql.connect(host=settings['db_host'], 
                                    port=settings['db_port'], 
                                    user=settings['db_username'], 
                                    passwd=settings['db_password'], 
                                    db=settings['db_name'])
         except pymysql.err.InternalError, e:
             print "MySQL internal error - ", e[0], ": ", e[1]
             pass

    @staticmethod
    def query_filekey(key, con=dbconnect()):
        cursor = con.cursor()
        query = (key,)
        if db_type == 'sqlite':
            cursor.execute('select * from files where fkey=?', query)
        elif db_type == 'mysql':
            cursor.execute('select * from files where fkey=%s', query)
        try:
            file_path = cursor.fetchone()[1]
        except TypeError:
            return False
        except sqlite3.Error, e:
            print e
        return file_path
    @staticmethod
    def query_files_user(user, con=dbconnect()):
        cursor = con.cursor()
        query = (user,)
        if db_type == 'sqlite':
            cursor.execute('select * from files where user=?', query)
        elif db_type == 'mysql':
            cursor.execute('select * from files where user=%s', query)
        return cursor.fetchall()
    @staticmethod
    def insert_file(filepath, user, con=dbconnect()):
        key=rand_alpha_numeric(14)
        date=time.asctime(time.gmtime())
        con = db.connect()
        try:
            cursor = con.cursor()
            query = (key, filepath, user, date,)
            print query
            if db_type == 'sqlite':
                cursor.execute('insert into files(fkey, path, user, time) values (?,?,?,?)', query)
            elif db_type == 'mysql':
                cursor.execute('insert into files(fkey, path, user, time) values (%s,%s,%s,%s)', query)
            con.commit()
        except pymysql.err.InternalError, e:
            print e[0],"  ",e[1]
            return None
        con.close()
        return key
    @staticmethod
    def query_user(user, passwd, con=dbconnect()):
        cursor = con.cursor()
        query = (hashlib.md5(user+passwd).hexdigest(),)
        if db_type == 'sqlite':
            cursor.execute('select * from users where hash=?', query)
        elif db_type == 'mysql':
            cursor.execute('select * from users where hash=%s', query)
        return cursor.fetchone()
    @staticmethod
    def add_user(user, passwd, email, premium='', verified=False):
        conn = db.connect()
        key = hashlib.md5(user+passwd).hexdigest()
        date=time.asctime(time.gmtime())
        #try:
        cursor = conn.cursor()
        query = (key, user, email, time.asctime(time.gmtime()), verified, premium)
        if db_type == 'sqlite':
            cursor.execute('insert into users(hash,name,email,datejoined,verified,premium) values (?,?,?,?,?,?)', query)
        elif db_type == 'mysql':
            cursor.execute('insert into users(hash,name,email,datejoined,verified,premium) values (%s,%s,%s,%s,%s,%s)', query)
        conn.commit()
        #except:
        #    return None
        return key
    @staticmethod
    def check_email_available(email, con=dbconnect()):
        cursor = con.cursor()
        query = (email,)
        if db_type == 'sqlite':
            cursor.execute('select * from users where email=?', query)
        elif db_type == 'mysql':
            cursor.execute('select * from users where email=%s', query)
        #if cursor.fetchone(): return False #return false if *not* available
        #else: return True
        return True
        