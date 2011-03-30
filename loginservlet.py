from webob import Request, Response
from sessionservlet import UserSession, Session
from templservlet import render
from dbservlet import db
import sqlite3

def LoginApp(environ, start_response, session=Session()):
    req = Request(environ)
    #print req.headers['cookies']
    if req.str_POST.has_key('user') and req.str_POST.has_key('pass'):
        thconn = sqlite3.connect('pfsdb')
        dbinfo = db.query_user(req.str_POST['user'], req.str_POST['pass'],thconn)
        if dbinfo:
            is_session = session.check_session(uphash=dbinfo[0])
            if is_session:
                res = login_response(session.get_session_data(uphash=dbinfo[0])['key'])
                return res(environ, start_response)
            else:
                sess = UserSession(session.gen_session_key(),dbinfo[0],req.remote_addr)
                key = session.add_session(sess)
                res = login_response(key)
                return res(environ, start_response)
        else:      
            res = login_not_found(req.remote_addr)
            return res(environ, start_response)
    else:
        res = login_page()
        return res(environ, start_response)
       
def login_response(session_key):
    """Make login successful page"""
    res = Response(content_type='text/html', conditional_response=True)
    if session_key:
        res.set_cookie('sessid', session_key, max_age=360, path='/', 
                       domain='localhost:8070', secure=True)
    res.headers.add('Server', 'JCT File Server 0.01')
    res.body = render() % ('Login Successful', 'You are now logged in.')
    res.etag = '%s' % hash(res.body)
    return res
def login_not_found(ip):
    """Make failed page"""
    res = Response(content_type='text/html', conditional_response=True, status='403')
    res.body = render() % ('Login Failed','User/Password Invalid.')
    res.headers.add('Server', 'JCT File Server 0.01')
    return res
def login_page():
    res = Response(content_type='text/html', conditional_response=True)
    res.body = render() % ('Login','<form action="/login" method="POST"><input name="user" type="text" class="textfield"><br><input name="pass" type="text" class="textfield"><br><input name="" type="submit" class="button" value="Login"></form>')
    res.headers.add('Server', 'JCT File Server 0.01')
    return res