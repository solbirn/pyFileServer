#!/usr/bin/env python
# -*- coding: utf-8
import cherrypy,sqlite3
import win32security
#from webob import Request, Response

#from sessionservlet import UserSession, SessionDB
from utilsservlet import settings
from templservlet import render
from dbservlet import db

class LoginApp(object):

    def index(self):
        if cherrypy.request.scheme == 'https' or not (settings.has_key('ssl_certificate') and settings.has_key('ssl_private_key')):
            return render(title='Login',content="""
            <form action="do" method="POST" style="padding-top:30px">
            <table width="300" align="center">
            <tr><td width="200px">Username: </td><td><input name="user" type="text" class="textfield"></td></tr>
            <tr><td width="200px">Password: </td><td><input name="passw" type="password" class="textfield"></td></tr>
            <tr><td></td><td align="right"><input name="submit" type="submit" class="button" value="Login"></td></tr>
            </table>
            </form>""")
        else:
            raise cherrypy.HTTPRedirect(["https://%s:%s/login/" % (settings['hostname'],settings['ssl_port'])], 302)
    index.exposed =  True
    def do(self, user, passw, domain='tech-keys', submit=None):
        if (cherrypy.session.get('login') == True) and (cherrypy.session.get('ip') == cherrypy.request.remote.ip):
            raise cherrypy.HTTPRedirect(["/upload/"], 302)
        #try:
        #    handle = win32security.LogonUser(user,domain,passw, win32security.LOGON32_LOGON_INTERACTIVE, win32security.LOGON32_PROVIDER_DEFAULT)
        #except:
        #    return render(title='Login Failed',content='User/Password Invalid.')
        #handle.Close()
        cherrypy.session['login'] = True;
        if '@' in user:
            user = user.split('@')[0]
        cherrypy.session['user'] = user;
        cherrypy.session['domain'] = domain;
        cherrypy.session['ip'] = cherrypy.request.remote.ip;
        cherrypy.session.save()
        raise cherrypy.HTTPRedirect(["http://%s:%s/batches/" % (settings['hostname'],settings['port'])], 302)
    do.exposed = True
    def end(self):
        cherrypy.session.expire()
        raise cherrypy.HTTPRedirect(["/login/"], 302)
    
class LogoutApp(object):
    
    def index(self):
        cherrypy.log.error("In Logout")
        cherrypy.session.delete()
        raise cherrypy.HTTPRedirect(["/login/"], 302)
    index.exposed = True

class BatchesApp(object):
    def index(self):
        if not (cherrypy.session.get('login') == True) and not (cherrypy.session.get('ip') == cherrypy.request.remote.ip):
            raise cherrypy.HTTPRedirect(["/login/"], 302)
        conn = sqlite3.connect(settings['db_name'])
        batches = db.query_batch_keys_for_user(cherrypy.session.get('user'), conn)
        conn.close()
        if batches:
            batchtmpl = """<table id="batches" align="center"><tr id="%s">
            <td width="200"><span>%s</span></td>
            <td>
            <div class="row fileupload-buttonbar">
                        <div class="span7">
                            <span class="btn btn-success fileinput-button" onclick="window.location = 'http://%s:%s/upload/?batch=%s'">
                                <i class="icon-plus icon-white"></i>
                                <span>Edit</span>
                            </span>
                            <span class="btn btn-primary start" onclick="window.location = 'http://%s:%s/file/%s'">
                                <i class="icon-upload icon-white"></i>
                                <span>Download</span>
                            </span>
                            <span class="btn btn-danger delete" title="Delete from batch and server" onclick="delete_key('%s')">
                                <i class="icon-trash icon-white"></i>
                                <span>Delete</span>
                            </span>
                        </div>
                    </div>
            </td>
            </tr>
            </table>"""
            batchhtml = ""
            for batch in batches:
                batchhtml += batchtmpl % (batch[0], batch[1], settings['hostname'],settings['port'],batch[0], settings['hostname'],settings['port'],batch[0], batch[0])
            return render(title=render('__server_info__'),content=batchhtml,login=True)
        else:
            return render(title=render('__server_info__'),content="""
            <div class="row" style="text-align:center;font-size:25px;padding-bottom:30px;color:grey;">Oops! You don't have any batches yet.</div>
            <div class="row" style="text-align:center;font-size:25px;padding-bottom:30px;color:grey;"><a href="/upload">Upload something here</a></div>""", login=True);
    index.exposed = True
    
    def change(self, key, name):
        if not (cherrypy.session.get('login') == True) and not (cherrypy.session.get('ip') == cherrypy.request.remote.ip):
            raise cherrypy.HTTPRedirect(["/login/"], 302)
        if name != '':
            conn = sqlite3.connect(settings['db_name'])
            r = db.change_batch_name(key, name, conn)
            conn.close()
    change.exposed = True
    
class Register(object):
    def index(self):
        return render(title='Register',content='<form action="do" method="POST"><input type="hidden" name="create" style="visibilty: hidden">Username: <input name="name" type="text" class="textfield"><br>Email: <input name="email" type="text" class="textfield"><br>Password: <input name="pass" type="text" class="textfield"><br><input name="" type="submit" class="button" value="Register"></form>')
    index.exposed = True
    
#===============================================================================
# def LoginApp(environ, start_response, session=SessionDB()):
#    req = Request(environ)
#    if req.str_POST.has_key('user') and req.str_POST.has_key('pass'):
#        thconn = sqlite3.connect(settings['db_name'])
#        
#        dbinfo = db.query_user(req.str_POST['user'], req.str_POST['pass'], thconn)
#        if dbinfo:
#            is_session = session.check_get(uphash=dbinfo[0])
#            if is_session:
#                res = login_response(is_session[0])
#                return res(environ, start_response)
#            else:
#                sess = UserSession(session.gen_session_key(),dbinfo[0],req.remote_addr)
#                key = session.add(sess)
#                res = login_response(key)
#                return res(environ, start_response)
#        else:      
#            res = login_page('Login Failed.<br>User or password Invalid.<br>',req.remote_addr)
#    elif req.str_POST.has_key('create'):
#        if req.str_POST.has_key('name') and req.str_POST.has_key('email') \
#        and req.str_POST.has_key('pass'):
#            thconn = sqlite3.connect(settings['db_name'])
#            is_available = db.check_email_available(req.str_POST['email'], thconn)
#            if is_available:
#                key = db.add_user(req.str_POST['name'], req.str_POST['pass'], req.str_POST['email'])
#                if not key: res = login_page("<div>Oops! An error has occured. Please try again later.</div>")
#                else: res = login_response(key, '<br>An email will be sent to you for validation.')
#            else: res = login_page('<div>The email you have tried to register with is already taken.</div>')
#        else: res = login_page("<div>Oops! An error has occured. Something you entered is invalid.</div>")          
#    else: res = login_page()
#    return res(environ, start_response)     
#===============================================================================
#===============================================================================
# 
# def login_response(session_key, message=''):
#    """Make login successful page"""
#    res = Response(content_type='text/html', conditional_response=True)
#    if session_key:
#        res.set_cookie('sessid', session_key, max_age=360, path='/', 
#                       domain='FALSE', secure=True)
#    res.headers.add('Server', render('__server_info__'))
#    body = render(title='Login Successful',content='You are now logged in.%s' % message)
#    res.body = body.encode()
#    res.etag = '%s' % hash(res.body)
#    return res
# def login_not_found(ip):
#    """Make failed page"""
#    res = Response(content_type='text/html', conditional_response=True, status='403')
#    res.body = render(title='Login Failed',content='User/Password Invalid.')
#    res.headers.add('Server', render('__server_info__'))
#    return res
# def login_page(message='',ip=''):
#    res = Response(content_type='text/html', conditional_response=True)
#    body = render(title='Login',content='%s<form action="/login" method="POST">Username: <input name="user" type="text" class="textfield"><br>Password: <input name="pass" type="text" class="textfield"><br><input name="" type="submit" class="button" value="Login"></form>' % message)
#    res.body = body.encode()
#    res.headers.add('Server', render('__server_info__'))
#    return res
#===============================================================================