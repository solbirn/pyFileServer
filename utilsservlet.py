def rand_alpha_numeric(length):
    import random, time
    word = ""
    random.seed()
    for i in range(1,length):
        word += random.choice('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890')
    return word

def create_db():
    import sqlite3
    conn = sqlite3.connect('pfsdb')
    c = conn.cursor()
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
        return os.path.expandvars("%USERPROFILE%\\Downloads\\")
    else:
        return os.path.expandvars("$HOME/Downloads/")

if __name__ == '__main__':
    import sys
    if len(sys) > 1:
        if sys.argv[1] == "--create-db":
            create_db()
