from utilsservlet import rand_alpha_numeric
import hashlib, time


class RamDB(object):
    def __init__(self):
        self.by_key = {}
        self.by_hash = {}
    def add(self, session):
        self.by_key.update({session.key:session})
        self.by_hash.update({session.uphash:session})
class Session:
    def __init__(self):
        self.db = RamDB()
    def add_session(self, session):
        self.db.add(session)
        return session.key
    def del_session(self, key=None, uphash=None):
        if key:
            del self.db.by_hash[self.db.by_key[key].uphash]
            del self.db.by_key[key]
            return True
        elif uphash:
            del self.db.by_key[self.db.by_hash[hash].key]
            del self.db.by_hash[uphash]
            return True
        else: return False
    def check_session(self, key=None, uphash=None):
        if key: return self.db.by_key.has_key(key)
        elif uphash: return self.db.by_hash.has_key(uphash)
        else: return None
    def get_session_data(self, key=None, uphash=None):
        if key: return self.db.by_key[key].data
        elif uphash: return self.db.by_hash[uphash].data
        else: return None
    def set_session_data(self, data, key=None, uphash=None):
        if key: self.db.by_key[key].data = data
        elif uphash: self.db.by_hash[uphash].data = data
        else: return None
    def gen_session_key(self):
        key = hashlib.sha256()
        key.update(rand_alpha_numeric(20))
        return key.hexdigest()
class UserSession(object):
    def __init__(self, key, uphash, ip, data={}, currtime=time.localtime()):
        self.creation_time = currtime
        self.key = key
        self.uphash = uphash
        self.ip = ip
        self.data = data