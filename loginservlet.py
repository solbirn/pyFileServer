from webob import Request, Response
from sessionservlet import UserSession
from templservlet import render
from dbservlet import db

def LoginApp(environ, start_response, session):
    req = Request(environ)
    if req.str_POST['user'] and req.str_POST['pass']:
        dbinfo = db.query_user(req.str_POST['user'], req.str_POST['pass'])
        if dbinfo:
            is_session = session.check_session(uphash=dbinfo[0])
            if is_session:
                res = login_response(session.get_session_data(uphash=dbinfo[0])['key'])
                return res(environ, start_response)
            else:
                res = login_response(session.db.add(UserSession(session.gen_session_key(),dbinfo[0],req.remote_addr)))
                return res(environ, start_response)
               
    res = login_not_found(req.remote_addr)
    return res(environ, start_response)
       
def login_response(session_key):
    res = Response(content_type='text/html', conditional_response=True)
    if session_key:
        res.headers['cookie'] = "sessid=%s" % session_key
    res.headers.add('Server', 'JCT File Server 0.01')
    res.body = render() % ('Login Successful', 'You are now logged in.')
    res.etag = '%s' % hash(res.body)
    return res
def login_not_found(ip):
    res = Response(content_type='text/html', conditional_response=True, status='403')
    res.body = render() % ('Login Failed','User/Password Invalid.')
    res.headers.add('Server', 'JCT File Server 0.01')
    return res