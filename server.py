import sys, cherrypy
from cherrypy import wsgiserver
from fileservlet import FileApp
from uploadservlet import *
from loginservlet import LoginApp
from templservlet import render

config = {'global':
    {
        'tools.staticfile.on': True,
        'tools.staticfile.filename': "favico.ico",
    }
}

class Main:
    def index(self):
        return render() % ('Home Page','Welcome!')
    index.exposed = True

class Icon:
    def index(self):
        return serve_file("favicon.ico", "image/x-icon", "attachment")
    index.exposed = True
    
def main():
    AppDispatcher = wsgiserver.WSGIPathInfoDispatcher({'/file': FileApp, 
                                                    '/login': LoginApp,
                                                    '/upload': cherrypy.tree.mount(UploadApp(),'/upload',config=config),
                                                    '/': cherrypy.tree.mount(Main(),'/',config=config),
                                                    '/favicon.ico': (Icon(),'/')})
    server = wsgiserver.CherryPyWSGIServer(
           ('127.0.0.1', 8090), AppDispatcher,
           server_name='JCT File Server 0.01', 
           numthreads=100, request_queue_size=70)
    try: server.start()
    except KeyboardInterrupt: sys.exit()

if __name__ == '__main__':
    main()

