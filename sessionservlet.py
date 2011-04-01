import hashlib, time, sqlite3

from utilsservlet import rand_alpha_numeric, create_db

#class RamDB(object):
#    def __init__(self):
#        self.by_key = {}
#        self.by_hash = {}
#    def add(self, session):
#        self.by_key.update({session.key:session})
#        self.by_hash.update({session.uphash:session})
#class Session:
#    def __init__(self):
#        self.db = RamDB()
#    def add_session(self, session):
#        self.db.add(session)
#        return session.key
#    def del_session(self, key=None, uphash=None):
#        if key:
#            del self.db.by_hash[self.db.by_key[key].uphash]
#            del self.db.by_key[key]
#            return True
#        elif uphash:
#            del self.db.by_key[self.db.by_hash[hash].key]
#            del self.db.by_hash[uphash]
#            return True
#        else: return False
#    def check_session(self, key=None, uphash=None):
#        if key: return self.db.by_key.has_key(key)
#        elif uphash: return self.db.by_hash.has_key(uphash)
#        else: return None
#    def get_session_data(self, key=None, uphash=None):
#        if key: return self.db.by_key[key].data
#        elif uphash: return self.db.by_hash[uphash].data
#        else: return None
#    def set_session_data(self, data, key=None, uphash=None):
#        if key: self.db.by_key[key].data = data
#        elif uphash: self.db.by_hash[uphash].data = data
#        else: return None
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
    def add(self, session):
        print session
        conn = sqlite3.connect("sess")
        cur = conn.cursor()
        cur.execute("insert into sessions values(?,?,?,?,?)", 
                    (session.key, session.uphash, session.ip, session.data, session.creation_time))
        conn.commit()
    def check_get(self, key=None, uphash=None):
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
            
        