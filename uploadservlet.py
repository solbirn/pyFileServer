import os, cherrypy, sqlite3

from utilsservlet import get_upload_path, settings
from templservlet import render
from dbservlet import db

class UploadApp(object):

    def index(self):
        return render(title="Upload",content="""
            <h2>Upload a file</h2>
            <form action="do" method="post" enctype="multipart/form-data">
            filename: <input type="file" name="myFile" /><br />
            <input type="submit" />
            </form>
        """)
    index.exposed = True

    def do(self, myFile):
        fpath = get_upload_path()+myFile.filename
        
        while os.path.exists(fpath):
            pathparts = fpath.split('.')
            pathparts[-2]+='_'
            fpath = ''
            for part in pathparts:
                fpath += part + '.'
            fpath = fpath[:-1]
            
        f = open(fpath,'wb')
        size = 0
        while True:
            data = myFile.file.read(8192)
            if not data:
                break
            f.write(data)
            size += len(data)
        f.close()
        conn = sqlite3.connect(settings['db_name'])
        key = db.insert_file(fpath, 'anonymous', conn)   
             
        hostaddr = cherrypy.request.local.ip
        hostport = cherrypy.request.local.port

        if hostaddr == '': 
            hostaddr = 'localhost'
        print hostaddr 
        if hostport != 80:
            absfilepath = '%s://%s:%s/file/%s/%s' % (cherrypy.request.scheme, hostaddr, hostport, key, myFile.filename)
        else:
            absfilepath = 'http://%s/file/%s/%s' % (hostaddr, key, myFile.filename)
        
        return render(title="Upload complete",content="""<h2>Upload Complete!</h2><br>
                                                        <div style="padding-left:15px;">The url for your file is:<br> %s</div>""" % absfilepath)
    do.exposed = True