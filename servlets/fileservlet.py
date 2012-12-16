#!/usr/bin/env python
# -*- coding: utf-8
import os, sqlite3, mimetypes, zipfile
from webob import Request, Response

from templservlet import render
from utilsservlet import settings, Zipper, rand_alpha_numeric, get_upload_path
from dbservlet import db

def FileApp(environ, start_response, struct=settings['serve_dir']):
    req = Request(environ)
    #===========================================================================
    # if struct:
    #    filename = 'C:%s' % req.path.replace('/file','').replace('/',os.path.sep)
    #    if os.path.isdir(filename):
    #        res = make_folder_response(filename, req)
    #        return res(environ, start_response)
    #    else:
    #        res = make_file_response(filename)
    #        return res(environ, start_response)
    # else:
    #===========================================================================
    filekey = req.path.replace('/file/','').split('/')[0]
    conn = sqlite3.connect(settings['db_name'])
    filename = db.query_filekey(filekey, conn)
    if filename:
        if os.path.isdir(filename):
            res = make_folder_response_zip(filename)
        elif os.path.isfile(filename):
            res = make_file_response(filename)
    else:
        res = Response(status='404')
        res.headers.add('Server', render('__server_info__'))
    return res(environ, start_response)

def get_mimetype(filename):
    mtype, encoding = mimetypes.guess_type(filename)
    return mtype or 'application/octet-stream'

def make_file_response(filename):
    res = Response(content_type=get_mimetype(filename),
                   conditional_response=True)
    res.headers.add('Accept-Ranges','bytes')
    res.headers.add('Server', render('__server_info__'))
    res.headers.add('Content-Disposition',str('attachment; filename=%s'%(filename.split(os.path.sep)[-1])))
    res.app_iter = FileIterable(filename)
    #try:
    res.content_length = os.path.getsize(filename)
    res.last_modified = os.path.getmtime(filename)
    res.etag = '%s-%s-%s' % (os.path.getmtime(filename),
                             os.path.getsize(filename), hash(filename))
    #===========================================================================
    # except WindowsError, e:
    #    if e.errno == 2:
    #        del res
    #        res = Response(status='404')
    #        res.headers.add('Server', render('__server_info__'))
    #===========================================================================
    return res
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
    res.headers.add('Server', render('__server_info__'))
    res.content_length = len(res.body)
    res.last_modified = os.path.getmtime(foldername)
    res.etag = '%s-%s-%s' % (os.path.getmtime(foldername),
                             os.path.getsize(foldername), hash(foldername))
    return res
def create_unique_temp_dir():
    if not (os.path.isdir(get_upload_path() + "temp")):
        os.mkdir(get_upload_path() + "temp")
    randdir = get_upload_path() + "temp" + os.path.sep + rand_alpha_numeric(10)
    os.mkdir(randdir)
    return randdir

def make_folder_response_zip(foldername):
    zip = Zipper()
    foldernames = foldername.split(os.path.sep)
    filename = create_unique_temp_dir() + os.path.sep + foldernames[-1] + '.zip'
    print 'a: ' + foldername, " ", filename
    zip.toZip(foldername, filename)
    return make_file_response(filename)

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
    chunk_size = 4092
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