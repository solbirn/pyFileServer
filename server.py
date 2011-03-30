import sys, cherrypy
from cherrypy import wsgiserver
from fileservlet import FileApp
from loginservlet import LoginApp
from templservlet import render


class Main:
    def index(self):
        return render() % ('Home Page','Welcome!')
    index.exposed = True

    
def main():
    AppDispatcher = wsgiserver.WSGIPathInfoDispatcher({'/file': FileApp, 
                                                    '/login': LoginApp,
                                                    '/': cherrypy.tree.mount(Main(),'/')})
    server = wsgiserver.CherryPyWSGIServer(
           ('127.0.0.1', 8070), AppDispatcher,
           server_name='JCT File Server 0.01', 
           numthreads=100, request_queue_size=70)
    try: server.start()
    except KeyboardInterrupt: sys.exit()

if __name__ == '__main__':
    main()

