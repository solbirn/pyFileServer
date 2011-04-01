from templservlet import __settings__

def rand_alpha_numeric(length):
    import random, time
    word = ""
    random.seed()
    for i in range(1,length):
        word += random.choice('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890')
    return word

def create_db(db_name='pfsdb'):
    import sqlite3
    conn = sqlite3.connect(db_name)
    c = conn.cursor()
    if db_name == ":memory:" or db_name == "sess":
        c.executescript("""
        create table sessions(
            key key,
            hash,
            ip,
            crtime,
            data
            );
        """)
        conn.commit()
    else:
        c.executescript("""
        create table files(
            key key,
            path,
            user,
            time,
            errcode
        );
        
        create table users(
            hash key,
            name,
            email,
            datejoined,
            verified bool,
            premium
        );
        """)   
        conn.commit()

def get_upload_path():
    import os
    if os.name == 'nt':
        return os.path.expandvars(__settings__['uploaddir']['windows'])
    else:
        return os.path.expandvars(__settings__['uploaddir']['posix'])

if __name__ == '__main__':
    import sys
    if len(sys) > 1:
        if sys.argv[1] == "--create-db":
            create_db()
