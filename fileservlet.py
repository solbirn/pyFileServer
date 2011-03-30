from webob import Request, Response
from dbservlet import db
import mimetypes
import os, sqlite3

def FileApp(environ, start_response, struct='keysystem'):
    req = Request(environ)
    if struct == 'filesystem':
        filename = 'C:%s' % req.path.replace('/file','').replace('/',os.path.sep)
        if os.path.isdir(filename):
            res = make_folder_response(filename, req)
            return res(environ, start_response)
        else:
            res = make_file_response(filename)
            return res(environ, start_response)
    else:
        filekey = req.path.replace('/file/','').split('/')[0]
        conn = sqlite3.connect('pfsdb')
        filename = db.query_filekey(filekey, conn)
        res = make_file_response(filename)
        return res(environ, start_response)
    
#@staticmethod
def get_mimetype(filename):
    type, encoding = mimetypes.guess_type(filename)
    # We'll ignore encoding, even though we shouldn't really
    return type or 'application/octet-stream'

#@staticmethod
def make_file_response(filename):
    res = Response(content_type=get_mimetype(filename),
                   conditional_response=True)
    res.headers.add('Accept-Ranges','bytes')
    res.headers.add('Server', 'JCT File Server 0.01')
    res.headers.add('Content-Disposition','attachment; filename=%s'%(filename.split(os.path.sep)[-1]))
    res.app_iter = FileIterable(filename)
    res.content_length = os.path.getsize(filename)
    res.last_modified = os.path.getmtime(filename)
    res.etag = '%s-%s-%s' % (os.path.getmtime(filename),
                             os.path.getsize(filename), hash(filename))
    return res

#@staticmethod
def make_folder_response(foldername, req):
    if req.path_url.endswith('/'):
        fold_url = req.path_url[:-1]
    else:
        fold_url = req.path_url
    folderlist = [ '<html>' + #foldername +
                '<br>'.join( [('<a href="%s/%s">%s</a>' % (fold_url, filename, filename))
                                for filename in os.listdir(foldername)])
                                 + '</html>'   ]
    res = Response(content_type="text/html",
                   conditional_response=True)
    res.body = folderlist[0]
    res.headers.add('Server', 'pyFileServer 0.01')
    res.content_length = len(res.body)
    res.last_modified = os.path.getmtime(foldername)
    res.etag = '%s-%s-%s' % (os.path.getmtime(foldername),
                             os.path.getsize(foldername), hash(foldername))
    return res

class FileIterable(object):
    def __init__(self, filename, start=None, stop=None):
        self.filename = filename
        self.start = start
        self.stop = stop
    def __iter__(self):
        return FileIterator(self.filename, self.start, self.stop)
    def app_iter_range(self, start, stop):
        return self.__class__(self.filename, start, stop)
class FileIterator(object):
    chunk_size = 4096
    def __init__(self, filename, start, stop):
        self.filename = filename
        self.fileobj = open(self.filename, 'rb')
        if start:
            self.fileobj.seek(start)
        if stop is not None:
            self.length = stop - start
        else:
            self.length = None
    def __iter__(self):
        return self
    def next(self):
        if self.length is not None and self.length <= 0:
            raise StopIteration
        chunk = self.fileobj.read(self.chunk_size)
        if not chunk:
            raise StopIteration
        if self.length is not None:
            self.length -= len(chunk)
            if self.length < 0:
                # Chop off the extra:
                chunk = chunk[:self.length]
        return chunk