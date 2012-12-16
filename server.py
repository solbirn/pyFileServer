#!/usr/bin/env python
# -*- coding: utf-8
import os, sys, cherrypy, thread
from cherrypy.wsgiserver import WSGIPathInfoDispatcher, CherryPyWSGIServer
#from cherrypy.process.plugins import Daemonizer
from cherrypy.process.servers import *

from servlets.fileservlet import FileApp
from servlets.uploadservlet import UploadApp
from servlets.loginservlet import LoginApp, LogoutApp, BatchesApp
from servlets.utilsservlet import create_db, settings, err_pages, check_create_db
from servlets.templservlet import render

config = {'/':
    {
        'tools.staticdir.root' : os.getcwd(),
        'tools.sessions.on' : True,
        'tools.sessions.storage_type' : "file",
        'tools.sessions.storage_path' : os.getcwd() + os.path.sep + 'sessions',
        'tools.sessions.timeout' : 60
    }, 
        '/favicon.ico':
    {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "%s\\favicon.ico" % os.getcwd(),
    },
        '/static':
    {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': "static",
        'tools.gzip.mime_types': """['text/*','image/*']"""
    }, 
          '/certs':
    {
        'tools.staticdir.on': True,
        'tools.staticdir.dir': "certs",
        'tools.gzip.mime_types': """['application/x-download']"""
    }
}

class Download:

    def index(self, filepath):
        from cherrypy.lib.static import serve_file
        return serve_file(filepath, "application/x-download", "attachment")
    index.exposed = True

class Main:
    #register = Register()
    upload = UploadApp()
    login = LoginApp()
    logout = LogoutApp()
    batches = BatchesApp()
    def index(self):
        return render(title=render('__server_info__'),content="""<ul style="list-style:none">
                                            <li><a href="/login">Login</a></li>
                                            <li><a href="/batches">My Batches</a></li>
                                            <li><a href="/upload">Upload a file</a></li>
                                            </ul>""")
    index.exposed = True

def main():
    cherrypy.config.update({'error_page.404': err_pages.err_404})
    # = Daemonizer(cherrypy.engine)
    #d.subscribe()
    AppDispatcher = WSGIPathInfoDispatcher({'/': cherrypy.tree.mount(Main(),'/',config=config),
                                            #'/login': LoginApp,
                                            '/file': FileApp
                                            })
    server = CherryPyWSGIServer(
                                (settings['ip'], settings['port']), 
                                AppDispatcher,
                                server_name=render('__server_info__'), 
                                numthreads=100, 
                                request_queue_size=70
                                )

    serverSSL = None
    
    if settings.has_key('ssl_certificate') and settings.has_key('ssl_private_key'):
        if os.path.exists(settings['ssl_certificate']) and os.path.exists(settings['ssl_private_key']):
                serverSSL = CherryPyWSGIServer(
                               (settings['ip'], settings['sslport']), 
                               AppDispatcher,
                               server_name=render('__server_info__'), 
                               numthreads=100, 
                               request_queue_size=70
                               )
                serverSSL.ssl_certificate = settings['ssl_certificate']
                serverSSL.ssl_private_key = settings['ssl_private_key']
                s2 = ServerAdapter(cherrypy.engine, serverSSL)
                s2.subscribe()
    s1 = ServerAdapter(cherrypy.engine, server)
    s1.subscribe()
    check_create_db(settings['db_name'],settings['db_name'])
    cherrypy.engine.timeout_monitor.unsubscribe()
    cherrypy.engine.start()
    cherrypy.engine.block()

    
if __name__ == '__main__':
    main()


