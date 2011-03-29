import random

def rand_alpha_numeric(length):
    word = ""
    for i in range(1,length):
        word += random.choice('qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM1234567890')
    return word

#class dbSession:
#    def __init__(self):
#        self.conn = sqlite3.connect('session.db')
#        self.conn.connect()
#    def check(self, session_key, ip):
#        cursor = self.conn.cursor()
#        query = (session_key,)
#        cursor.execute('select * from current where session_id=?',query)
#        if cursor is None:
#            return None
#        elif cursor[2] != ip:
#            return 'N'
#        else:
#            return cursor
#    def check_create(self, session_key, ip, uphash):
#        result = self.check(session_key, ip)
#        if result is not None:
#            if result is 'N':
#                self.delete_sessions_by_user(uphash)
#                return self.create_session(uphash, ip)
#            else:
#                return result[0]
#        else:
#            return self.create_session(uphash, ip)
#    def delete_sessions_by_user(self, uphash):
#        cursor = self.conn.cursor()
#        query = (uphash,)
#        cursor.execute('delete * from current where hash=?',query)
#    def create_session(self, uphash, ip):
#        new_key = self.gen_key()
#        cursor = self.conn.cursor()
#        query = (new_key, uphash, ip)
#        cursor.execute('insert into current values (?,?,?)',query)
