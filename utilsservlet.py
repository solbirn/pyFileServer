from templservlet import render

def rand_alpha_numeric(length):
    import random, time
    word = ""
    random.seed()
    for i in range(1,length):
        word += random.choice('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890')
    return word

def import_settings(path='pfs.conf'):
    settings = {}
    with open(path) as fHandle:
        linenum = 1
        for line in fHandle:
            setting = line.strip().split('#')[0].split('=')
            try:
                if setting[0] == '' or setting[1] == '':
                    linenum+=1
                    continue
                settings.update({setting[0]:setting[1]})
            except IndexError:
                print 'A line in the config file is not properly formatted:\n--Line %d: %s' % (linenum, line)
            linenum+=1
    if not settings.has_key('ip'):
        setting.update({'ip':'127.0.0.1'})
    if not settings.has_key('port'):
        setting.update({'port':80})
    else:
        settings['port'] = int(settings['port'])
    if not settings.has_key('db_name'):
        print 'Database name empty: Assuming database name is "pfsdb".'
        settings.update({'db_name':'pfsdb'})
    if not settings.has_key('db_type'):
        settings.update({'db_type':'sqlite'})
        print 'Using SQLite as Database server.'
    else:
        if settings['db_type'] == 'mysql':
            print 'Using MySQL as Database server.'
            if not settings.has_key('db_username'):
                print 'MySQL username missing. Fix and try again.'
                sys.exit(1) 
            if not settings.has_key('db_password'):
                print 'MySQL password missing. Fix and try again.'
                sys.exit(1) 
            if not settings.has_key('db_host'):
                print 'MySQL host ip/name missing. Fix and try again.'
                sys.exit(1)
            if not settings.has_key('db_port'):
                print 'MySQL port number missing. Fix and try again.'
                sys.exit(1)
            else: settings['db_port'] = int(settings['db_port'])
    if not settings.has_key('upload_dir'):
        import os
        if os.name == 'nt':
            settings.update({'upload_dir':os.path.expandvars("%USERPROFILE%\\Downloads\\")})
        else:
            settings.update({'upload_dir':os.path.expandvars("$HOME/Downloads/")})
    else:
        import os
        settings['upload_dir'] = os.path.expandvars(settings['upload_dir'])
    if not settings.has_key('serve_dir'):
        settings.update({'serve_dir':False})
    else:
        if settings['serve_dir'] == '0' or settings['serve_dir'].lower() == 'false':
            settings['serve_dir'] = False
        elif settings['serve_dir'] == '1' or settings['serve_dir'].lower() == 'true':
            settings['serve_dir'] = True
    if not settings.has_key('hostname'):
        settings.update({'hostname':'localhost'})
    return settings

settings = import_settings()

def create_db(db_name=settings['db_name']):
    from dbservlet import db
    conn = db.connect(db_name)
    c = conn.cursor()
    if settings['db_type'] == 'sqlite':
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
                fkey,
                path,
                user,
                time,
                errcode
            );
            
            create table users(
                hash,
                name,
                email,
                datejoined,
                verified bool,
                premium
            );
            
            create table dl_auth_by_ip(
                user,
                ip,
                perm_key
            );
            """)   
    elif settings['db_type'] == 'mysql':
        c.execute("""
        CREATE TABLE IF NOT EXISTS files(
            fkey VARCHAR(30) CHARSET utf8 PRIMARY KEY,
            path VARCHAR(200) CHARSET utf8,
            user VARCHAR(20) CHARSET utf8,
            time VARCHAR(24) CHARSET utf8,
            errcode SMALLINT UNSIGNED
        );
        
        CREATE TABLE IF NOT EXISTS users(
            hash CHAR(32) CHARSET utf8 PRIMARY KEY,
            name VARCHAR(20) CHARSET utf8,
            email VARCHAR(30) CHARSET utf8,
            datejoined CHAR(24) CHARSET utf8,
            verified BOOL,
            premium BOOL
        );
        
        CREATE TABLE IF NOT EXISTS dl_auth_by_ip(
            user VARCHAR(20) CHARSET utf8,
            ip VARCHAR(15) CHARSET utf8,
            perm_key VARCHAR(32) CHARSET utf8 PRIMARY KEY
        );
        """)
        conn.commit()

def get_upload_path():
    return settings['upload_dir']
    
class err_pages:
    @staticmethod
    def err_404(status, message, traceback, version):
        return render(title='404 Not Found', content="Oops! The page you are looking for doesn't exist<br>%s" % status)

def emailer(subject, to, message, efrom='no-reply@%s' % settings['hostname']):
    import smtplib
    from email.mime.text import MIMEText
    
    msg = MIMEText(message)
    
    msg['Subject'] = subject
    msg['From'] = efrom
    msg['To'] = to

    s = smtplib.SMTP('localhost')
    s.sendmail(efrom, [to], msg.as_string())
    s.quit()

#Run this script (utilsservlet.py) by itself with --create-db argument to create the database and table
#Note: If you are using MySQL you must create the database first and this script will create the tables

if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1:
        if sys.argv[1] == "--create-db":
            create_db()
        elif (sys.argv[1] == "--help") or (sys.argv[1] == "-h") \
         or (sys.argv[1] == "/h") or (sys.argv[1] == "/help"):
            print 'Usage: utilsservlet.py [--create-db]\nDo NOT delete this file. It contains may functions that are necessary for the correct execution of the server.'
