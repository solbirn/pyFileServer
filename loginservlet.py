import sqlite3
from webob import Request, Response

from sessionservlet import UserSession, SessionDB
from utilsservlet import settings
from templservlet import render
from dbservlet import db

class Register:
    def index(self):
        return render(title='Register',content='<form action="/login" method="POST"><input type="hidden" name="create" style="visibilty: hidden">Username: <input name="name" type="text" class="textfield"><br>Email: <input name="email" type="text" class="textfield"><br>Password: <input name="pass" type="text" class="textfield"><br><input name="" type="submit" class="button" value="Register"></form>')
    index.exposed = True

def LoginApp(environ, start_response, session=SessionDB()):
    req = Request(environ)
    if req.str_POST.has_key('user') and req.str_POST.has_key('pass'):
        thconn = sqlite3.connect(settings['db_name'])
        dbinfo = db.query_user(req.str_POST['user'], req.str_POST['pass'], thconn)
        if dbinfo:
            is_session = session.check_get(uphash=dbinfo[0])
            if is_session:
                res = login_response(is_session[0])
                return res(environ, start_response)
            else:
                sess = UserSession(session.gen_session_key(),dbinfo[0],req.remote_addr)
                key = session.add(sess)
                res = login_response(key)
                return res(environ, start_response)
        else:      
            res = login_page('Login Failed.<br>User or password Invalid.<br>',req.remote_addr)
    elif req.str_POST.has_key('create'):
        if req.str_POST.has_key('name') and req.str_POST.has_key('email') \
        and req.str_POST.has_key('pass'):
            thconn = sqlite3.connect(settings['db_name'])
            is_available = db.check_email_available(req.str_POST['email'], thconn)
            if is_available:
                key = db.add_user(req.str_POST['name'], req.str_POST['pass'], req.str_POST['email'])
                if not key: res = login_page("<div>Oops! An error has occured. Please try again later.</div>")
                else: res = login_response(key, '<br>An email will be sent to you for validation.')
            else: res = login_page('<div>The email you have tried to register with is already taken.</div>')
        else: res = login_page("<div>Oops! An error has occured. Something you entered is invalid.</div>")          
    else: res = login_page()
    return res(environ, start_response)     

def login_response(session_key, message=''):
    """Make login successful page"""
    res = Response(content_type='text/html', conditional_response=True)
    if session_key:
        res.set_cookie('sessid', session_key, max_age=360, path='/', 
                       domain='FALSE', secure=True)
    res.headers.add('Server', render('__server_info__'))
    body = render(title='Login Successful',content='You are now logged in.%s' % message)
    res.body = body.encode()
    res.etag = '%s' % hash(res.body)
    return res
def login_not_found(ip):
    """Make failed page"""
    res = Response(content_type='text/html', conditional_response=True, status='403')
    res.body = render(title='Login Failed',content='User/Password Invalid.')
    res.headers.add('Server', render('__server_info__'))
    return res
def login_page(message='',ip=''):
    res = Response(content_type='text/html', conditional_response=True)
    body = render(title='Login',content='%s<form action="/login" method="POST">Username: <input name="user" type="text" class="textfield"><br>Password: <input name="pass" type="text" class="textfield"><br><input name="" type="submit" class="button" value="Login"></form>' % message)
    res.body = body.encode()
    res.headers.add('Server', render('__server_info__'))
    return res