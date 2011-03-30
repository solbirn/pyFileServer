import os
localDir = os.path.dirname(__file__)
absDir = os.path.join(os.getcwd(), localDir)

from utilsservlet import get_upload_path
from dbservlet import db
import cherrypy, sqlite3

class UploadApp(object):

    def index(self):
        return """
        <html><body>
            <h2>Upload a file</h2>
            <form action="do" method="post" enctype="multipart/form-data">
            filename: <input type="file" name="myFile" /><br />
            <input type="submit" />
            </form>
            <h2>Download a file</h2>
            <a href='download'>This one</a>
        </body></html>
        """
    index.exposed = True

    def do(self, myFile):
        out = """<html>
        <body>
            myFile length: %s<br />
            myFile filename: %s<br />
            myFile mime-type: %s
        </body>
        </html>"""

        fpath = get_upload_path()+myFile.filename
        
        while os.path.exists(fpath):
            pathparts = fpath.split('.')
            pathparts[-2]+='_'
            fpath = ''
            for part in pathparts:
                fpath += part + '.'
            fpath = fpath[:-1]
            print fpath
            
        f = open(fpath,'wb')
        size = 0
        while True:
            data = myFile.file.read(8192)
            if not data:
                break
            f.write(data)
            size += len(data)
        f.close()
        conn = sqlite3.connect('pfsdb')
        key = db.insert_file(fpath, 'shlomo', conn)   
             
        hostaddr = cherrypy.request.local.ip
        hostport = cherrypy.request.local.port

        if hostaddr == '': 
            hostaddr = 'localhost'

        if hostport != 80:
            absfilepath = '%s://%s:%s/file/%s/%s' % (cherrypy.request.scheme, hostaddr, hostport, key, myFile.filename)
        else:
            absfilepath = 'http://%s/file/%s/%s' % (host, keyaddr, myFile.filename)
        
        return absfilepath
    do.exposed = True