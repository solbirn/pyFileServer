#!/usr/bin/env python
# -*- coding: utf-8
import hashlib, time, sqlite3
try: import pymysql
except: pass
from utilsservlet import rand_alpha_numeric, settings

def connect(db_name=settings['db_name']):
        if db_type == 'sqlite':
            try:
                return sqlite3.connect(db_name, check_same_thread = False)
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

conn = None
db_type = settings['db_type']

class db:
    @staticmethod
    def query_filekey(key, con=connect()):
        cursor = con.cursor()
        query = (key,)
        if db_type == 'sqlite':
            cursor.execute('select * from files where fkey=?', query)
        elif db_type == 'mysql':
            cursor.execute('select * from files where fkey=%s', query)
        try:
            file_path = cursor.fetchone()[2]
        except TypeError:
            return False
        except sqlite3.Error, e:
            print e
        #print file_path    
        return file_path
    @staticmethod
    def query_batch_key_for_files(key, con=connect()):
        cursor = con.cursor()
        query = (key,)
        if db_type == 'sqlite':
            cursor.execute('select * from files where rkey=?', query)
        elif db_type == 'mysql':
            cursor.execute('select * from files where rkey=%s', query)
        try:
            batches = cursor.fetchall()
        except TypeError:
            return False
        except sqlite3.Error, e:
            print e
        #print "BATCH: ", batches
        return batches
    @staticmethod
    def query_batch_keys_for_user(user, con=connect()):
        cursor = con.cursor()
        query = (user,)
        if db_type == 'sqlite':
            cursor.execute('select * from files where user=? and fkey=rkey', query)
        elif db_type == 'mysql':
            cursor.execute('select * from files where user=%s and fkey=rkey', query)
        try:
            batches = cursor.fetchall()
        except TypeError:
            return False
        except sqlite3.Error, e:
            print e
        #print "BATCH: ", batches
        return batches
    @staticmethod
    def delete_filekey(key, con=connect()):
        cursor = con.cursor()
        query = (key,)
        dquery = (key, key, )
        #print "Deleting fkey=", key
        if db_type == 'sqlite':
            if cursor.execute('select * from files where fkey=? and rkey=?', dquery):
                cursor.execute('delete from files where rkey=?', query)
            else:
                cursor.execute('delete from files where fkey=?', query)
        elif db_type == 'mysql':
            cursor.execute('delete from files where fkey=%s', query)
        try:
            con.commit()
            file_path = cursor.fetchone()[1]
        except TypeError:
            return False
        except sqlite3.Error, e:
            print e
        return file_path
    @staticmethod
    def change_batch_name(key, name, con=connect()):
        cursor = con.cursor()
        query = (name, key, key, )
        if db_type == 'sqlite':
            cursor.execute('update files set name=? where fkey=? and rkey=?', query)
        elif db_type == 'mysql':
            cursor.execute('update files set name=%s where fkey=%s and rkey=%s', query)
        try:
            con.commit()
            fetch = cursor.fetchone()[1]
        except TypeError:
            return False
        except sqlite3.Error, e:
            print e
        return fetch
    @staticmethod
    def query_files_user(user, con=connect()):
        cursor = con.cursor()
        query = (user,)
        if db_type == 'sqlite':
            cursor.execute('select * from files where user=?', query)
        elif db_type == 'mysql':
            cursor.execute('select * from files where user=%s', query)
        return cursor.fetchall()
    @staticmethod
    def insert_file(filepath, user, con=connect(), rkey='0',mkey=None):
        #print db_type
        if not mkey:
            key=rand_alpha_numeric(15)
        else:
            key = mkey
        date=time.asctime(time.gmtime())
        con = connect()
        #try:
        cursor = con.cursor()
        query = (key, key, filepath, user, date, rkey)
        #print query
        if db_type == 'sqlite':
            cursor.execute('insert into files(fkey, name, path, user, time, rkey) values (?,?,?,?,?,?)', query)
        elif db_type == 'mysql':
            cursor.execute('insert into files(fkey, name, path, user, time, rkey) values (%s,%s,%s,%s,%s,%s)', query)
        con.commit()
        #except pymysql.err.InternalError, e:
        #    print e[0],"  ",e[1]
        #    return None
        con.close()
        return key
    @staticmethod
    def query_user(user, passwd, con=connect()):
        cursor = con.cursor()
        query = (hashlib.md5(user+passwd).hexdigest(),)
        if db_type == 'sqlite':
            cursor.execute('select * from users where hash=?', query)
        elif db_type == 'mysql':
            cursor.execute('select * from users where hash=%s', query)
        return cursor.fetchone()
    @staticmethod
    def add_user(user, passwd, email, premium='', verified=False):
        conn = connect()
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
    def check_email_available(email, con=connect()):
        cursor = con.cursor()
        query = (email,)
        if db_type == 'sqlite':
            cursor.execute('select * from users where email=?', query)
        elif db_type == 'mysql':
            cursor.execute('select * from users where email=%s', query)
        #if cursor.fetchone(): return False #return false if *not* available
        #else: return True
        return True
        