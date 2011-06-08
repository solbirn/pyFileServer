import os, sys, cherrypy
from cherrypy.wsgiserver import WSGIPathInfoDispatcher, CherryPyWSGIServer

from fileservlet import FileApp
from uploadservlet import UploadApp
from loginservlet import LoginApp, Register
from utilsservlet import create_db, settings, err_pages
from templservlet import render

config = {'/favicon.ico':
    {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "%s\\favicon.ico" % os.getcwd(),
    },
        '/icon.png':
    {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "%s\\icon.png" % os.getcwd(),
    }
}

class Main:
    register = Register()
    upload = UploadApp()
    def index(self):
        return render(title=render('__server_info__'),content="""<ul style="list-style:none">
                                            <li><a href="/login">Login</a></li>
                                            <li><a href="/register">Register</a></li>
                                            <li><a href="/upload">Upload a file</a></li>
                                            </ul>""")
    index.exposed = True

def main():
    cherrypy.config.update({'error_page.404': err_pages.err_404})
    AppDispatcher = WSGIPathInfoDispatcher({'/': cherrypy.tree.mount(Main(),'/',config=config),
                                            '/login': LoginApp,
                                            '/file': FileApp
                                            })
    server = CherryPyWSGIServer(
                                (settings['ip'], settings['port']), 
                                AppDispatcher,
                                server_name=render('__server_info__'), 
                                numthreads=100, 
                                request_queue_size=70
                                )

    if settings.has_key('ssl_certificate') and settings.has_key('ssl_private_key'):
            if os.path.exists(settings['ssl_certificate']) and os.path.exists(settings['ssl_private_key']):
                server.ssl_certificate = os.path.exists(settings['ssl_certificate'])
                server.ssl_private_key = os.path.exists(settings['ssl_private_key'])
    else: print 'No SSL or not configured correctly.'

    
    try: server.start()
    except KeyboardInterrupt: sys.exit()

if __name__ == '__main__':
    main()

