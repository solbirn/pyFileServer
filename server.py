import os, sys, cherrypy
from cherrypy.wsgiserver import WSGIPathInfoDispatcher, CherryPyWSGIServer

from fileservlet import FileApp
from uploadservlet import UploadApp
from loginservlet import LoginApp, Register
from utilsservlet import create_db
from templservlet import render

config = {'/favicon.ico':
    {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "%s\\favicon.ico" % os.getcwd(),
    }
}

class Main:
    register = Register()
    upload = UploadApp()
    def index(self):
        from templservlet import render
        return render() % ('Home Page',"""<ul>
                                            <li><a href="/login">Login</a></li>
                                            <li><a href="/register">Register</a></li>
                                            <li><a href="/upload">Upload a file</a></li>
                                          </ul>""")
    index.exposed = True

def main():
    AppDispatcher = WSGIPathInfoDispatcher({'/': cherrypy.tree.mount(Main(),'/',config=config),
                                            '/login': LoginApp,
                                            '/file': FileApp
                                            })
    server = CherryPyWSGIServer(
                                ('127.0.0.1', 80), 
                                AppDispatcher,
                                server_name=render('__server_info__'), 
                                numthreads=100, 
                                request_queue_size=70
                                )
    try: server.start()
    except KeyboardInterrupt: sys.exit()

if __name__ == '__main__':
    main()

