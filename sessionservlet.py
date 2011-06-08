import hashlib, time, sqlite3

from utilsservlet import rand_alpha_numeric, create_db

try:
    create_db("sess")
except:
    pass

class UserSession(object):
    def __init__(self, key, uphash, ip, data='', currtime=time.asctime(time.gmtime())):
        self.creation_time = currtime
        self.key = key
        self.uphash = uphash
        self.ip = ip
        self.data = data
    def __str__(self):
        return "%s\n%s\n%s\n%s\n%s" % (self.key, self.uphash, self.ip, self.data, self.creation_time)

class SessionDB:
    @staticmethod
    def add(session):
        print session
        conn = sqlite3.connect("sess")
        cur = conn.cursor()
        cur.execute("insert into sessions values(?,?,?,?,?)", 
                    (session.key, session.uphash, session.ip, session.data, session.creation_time))
        conn.commit()
        del session
    @staticmethod
    def check_get(key=None, uphash=None):
        conn = sqlite3.connect("sess")
        cur = conn.cursor()
        if key:
            cur.execute("""select * from sessions where key=?""", (key,))
            return cur.fetchone()
        elif uphash:
            cur.execute("""select * from sessions where hash=?""", (uphash,))
            return cur.fetchone()
    @staticmethod
    def gen_session_key():
        key = hashlib.sha256()
        key.update(rand_alpha_numeric(20))
        return key.hexdigest()
            
        