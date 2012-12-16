#!/usr/bin/env python
# -*- coding: utf-8

import os, cherrypy, sqlite3, json

from utilsservlet import get_upload_path, settings, rand_alpha_numeric
from templservlet import render
from dbservlet import db


class UploadApp(object):

    def single(self):
        if not (cherrypy.session.get('login') == True) and not (cherrypy.session.get('ip') == cherrypy.request.remote.ip):
            raise cherrypy.HTTPRedirect(["/login/"], 302)
        return render(title="Upload",content="""
            <h2>Upload a file</h2>
            <form action="do" method="post" enctype="multipart/form-data">
            filename: <input type="file" name="myFile" /><br />
            <input type="submit" />
            </form>
        """)
    single.exposed = True
    
    def dosingle(self, myFile):
        if not (cherrypy.session.get('login') == True) and not (cherrypy.session.get('ip') == cherrypy.request.remote.ip):
            raise cherrypy.HTTPRedirect(["/login/"], 302)
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
        key = db.insert_file(fpath, cherrypy.session.get('user'), conn)   
             
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
    dosingle.exposed = True
    
    def index(self, batch=None):
        if not (cherrypy.session.get('login') == True) and not (cherrypy.session.get('ip') == cherrypy.request.remote.ip):
            raise cherrypy.HTTPRedirect(["/login/"], 302)
        if cherrypy.request.scheme == 'https':
            raise cherrypy.HTTPRedirect(["http://files.tech-keys.com:446/upload/"], 302)
        if batch:
            mkey = batch
        else:
            mkey = rand_alpha_numeric(15)
        return render(title="Upload", content="""
        <div class="container">
            <!-- The file upload form used as target for the file upload widget -->
            <form id="fileupload" action="http://"""+settings['hostname']+':'+str(settings['port'])+"""/upload/do" method="post" enctype="multipart/form-data">
                <div class="row" style="text-align:center;font-size:30px;padding-bottom:15px;line-height:33px;">Download entire batch (zip): <a href="http://"""+settings['hostname']+':'+str(settings['port'])+"""/file/"""+mkey+"""">http://"""+settings['hostname']+':'+str(settings['port'])+"""/file/"""+mkey+"""</a></div>
                <div class="row" style="text-align:center;font-size:20px;padding-bottom:20px;"><a href="javascript:delete_key('"""+mkey+"""')">Delete the entire batch</a></div>
                <div class="row" style="text-align:center;font-size:20px;padding-bottom:20px;">Friendly name: <input id="batchname" type="text" class="textfield"></div>
                <!-- The fileupload-buttonbar contains buttons to add/delete files and start/cancel the upload -->
                <div class="row fileupload-buttonbar centered">
                    <div class="span7">
                        <!-- The fileinput-button span is used to style the file input field as button -->
                        <span class="btn btn-success fileinput-button">
                            <i class="icon-plus icon-white"></i>
                            <span>Add files...</span>
                            <input type="file" name="myFile" multiple="">
                        </span>
                        <span class="btn btn-success fileinput-button">
                            <i class="icon-plus icon-white"></i>
                            <span>Add folder...</span>
                            <input type="file" name="myFile" multiple="" webkitdirectory="true" directory="" title="Only works with Google Chrome 11+">
                        </span>
                        <button type="submit" class="btn btn-primary start">
                            <i class="icon-upload icon-white"></i>
                            <span>Start upload</span>
                        </button>
                        <button type="reset" class="btn btn-warning cancel">
                            <i class="icon-ban-circle icon-white"></i>
                            <span>Cancel upload</span>
                        </button>
                        <button type="button" class="btn btn-danger delete" title="Delete from batch and server">
                            <i class="icon-trash icon-white"></i>
                            <span>Delete</span>
                        </button>
                        <input type="checkbox" class="toggle" title="Select all">
                        <input type="hidden" id="key" name="key" value=\""""+mkey+"""\">
                    </div>
                </div>
               <br>
                <!-- The loading indicator is shown during image processing -->
                <div class="row" style="text-align:center;font-size:25px;padding-bottom:30px;color:grey;" title="Folders not yet supported by browers. IE not supported.">Drag and drop files below</div>
                
                 <div class="row fileupload-buttonbar centered">
                    <div class="span5" style="width:100%; text-align:center; margin:0px;">
                        <!-- The global progress bar -->
                        <div class="progress progress-success progress-striped active fade">
                            <div class="bar" style="width:0%;"></div>
                        </div>
                    </div>
                </div>
                <div class="fileupload-loading"></div>
                <br>
                <!-- The table listing the files available for upload/download -->
                <table class="table table-striped"><tbody class="files" data-toggle="modal-gallery" data-target="#modal-gallery"></tbody></table>
            </form>
            
            
        </div>
        <!-- modal-gallery is the modal dialog used for the image gallery -->
        <div id="modal-gallery" class="modal modal-gallery hide fade" data-filter=":odd">
            <div class="modal-header">
                <a class="close" data-dismiss="modal"></a>
                <h3 class="modal-title"></h3>
            </div>
            <div class="modal-body"><div class="modal-image"></div></div>
            <div class="modal-footer">
                <a class="btn modal-download" target="_blank">
                    <i class="icon-download"></i>
                    <span>Download</span>
                </a>
                <a class="btn btn-success modal-play modal-slideshow" data-slideshow="5000">
                    <i class="icon-play icon-white"></i>
                    <span>Slideshow</span>
                </a>
                <a class="btn btn-info modal-prev">
                    <i class="icon-arrow-left icon-white"></i>
                    <span>Previous</span>
                </a>
                <a class="btn btn-primary modal-next">
                    <span>Next</span>
                    <i class="icon-arrow-right icon-white"></i>
                </a>
            </div>
        </div>
             <!-- The template to display files available for upload -->
        <script id="template-upload" type="text/x-tmpl">
        {% for (var i=0, file; file=o.files[i]; i++) { %}
            <tr class="template-upload fade">
                <td class="preview"><span class="fade"></span></td>
                <td class="name"><span>{%=file.name%}</span></td>
                <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
                {% if (file.error) { %}
                    <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
                {% } else if (o.files.valid && !i) { %}
                    <td>
                        <div class="progress progress-success progress-striped active"><div class="bar" style="width:0%;"></div></div>
                    </td>
                    <td class="start">{% if (!o.options.autoUpload) { %}
                        <button class="btn btn-primary">
                            <i class="icon-upload icon-white"></i>
                            <span>{%=locale.fileupload.start%}</span>
                        </button>
                    {% } %}</td>
                {% } else { %}
                    <td colspan="2"></td>
                {% } %}
                <td class="cancel">{% if (!i) { %}
                    <button class="btn btn-warning">
                        <i class="icon-ban-circle icon-white"></i>
                        <span>{%=locale.fileupload.cancel%}</span>
                    </button>
                {% } %}</td>
            </tr>
        {% } %}
        </script>
        <!-- The template to display files available for download -->
        <script id="template-download" type="text/x-tmpl">
        {% for (var i=0, file; file=o.files[i]; i++) { %}
            <tr class="template-download fade">
                {% if (file.error) { %}
                    <td></td>
                    <td class="name"><span>{%=file.name%}</span></td>
                    <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
                    <td class="error" colspan="2"><span class="label label-important">{%=locale.fileupload.error%}</span> {%=locale.fileupload.errors[file.error] || file.error%}</td>
                {% } else { %}
                    <td class="preview">{% if (file.thumbnail_url) { %}
                        <a href="{%=file.url%}" title="{%=file.name%}" rel="gallery" download="{%=file.name%}"><img src="{%=file.thumbnail_url%}"></a>
                    {% } %}</td>
                    <td class="name">
                        <a href="{%=file.url%}" title="{%=file.name%}" rel="{%=file.thumbnail_url&&'gallery'%}" download="{%=file.name%}">{%=file.name%}</a>
                    </td>
                    <td class="size"><span>{%=o.formatFileSize(file.size)%}</span></td>
                    <td colspan="2"></td>
                {% } %}
                <td class="delete">
                    <button class="btn btn-danger" data-type="{%=file.delete_type%}" data-url="{%=file.delete_url%}">
                        <i class="icon-trash icon-white"></i>
                        <span>{%=locale.fileupload.destroy%}</span>
                    </button>
                    <input type="checkbox" name="delete" value="1">
                </td>
            </tr>
        {% } %}
        </script>
        
        <!-- The jQuery UI widget factory, can be omitted if jQuery UI is already included -->
        <script src="/staticcache/js/vendor/jquery.ui.widget.js"></script>
        <!-- The Templates plugin is included to render the upload/download listings -->
        <script src="/staticcache/js/tmpl.min.js"></script>
        <!-- The Load Image plugin is included for the preview images and image resizing functionality -->
        <script src="/staticcache/js/load-image.min.js"></script>
        <!-- The Canvas to Blob plugin is included for image resizing functionality -->
        <script src="/staticcache/js/canvas-to-blob.min.js"></script>
        <!-- Bootstrap JS and Bootstrap Image Gallery are not required, but included for the demo -->
        <script src="/staticcache/js/bootstrap.min.js"></script>
        <script src="/staticcache/js/bootstrap-image-gallery.min.js"></script>
        <!-- The Iframe Transport is required for browsers without support for XHR file uploads -->
        <script src="/staticcache/js/jquery.iframe-transport.js"></script>
        <!-- The basic File Upload plugin -->
        <script src="/staticcache/js/jquery.fileupload.js"></script>
        <!-- The File Upload image processing plugin -->
        <script src="/staticcache/js/jquery.fileupload-ip.js"></script>
        <!-- The File Upload user interface plugin -->
        <script src="/staticcache/js/jquery.fileupload-ui.js"></script>
        <!-- The localization script -->
        <script src="/staticcache/js/locale.js"></script>
        <!-- The main application script -->
        <script src="/staticcache/js/main.js"></script>
        <!-- The XDomainRequest Transport is included for cross-domain file deletion for IE8+ -->
        <!--[if gte IE 8]><script src="/staticcache/js/cors/jquery.xdr-transport.js"></script><![endif]-->
        """, login=True)
    index.exposed = True
    
    def get(self, key):
        if cherrypy.request.method == 'GET':
            cherrypy.log.error("KEY: " + key)
            batch = db.query_batch_key_for_files(key)
            
            hostaddr = cherrypy.request.local.ip
            hostport = cherrypy.request.local.port
        
            if hostaddr == '': 
                hostaddr = settings['hostname']#'localhost'
            #print hostaddr 
            jobj = []
            conn = sqlite3.connect(settings['db_name'])
            for file in batch:
                fkey = file[0]
                filename = db.query_filekey(fkey, conn)
                size = os.path.getsize(filename)
                if hostport != 80:
                    absfilepath = '%s://%s:%s/file/%s/%s' % (cherrypy.request.scheme, hostaddr, hostport, fkey, filename.split(os.path.sep)[-1])
                    delurl = '%s://%s:%s/upload/delete?key=%s' % (cherrypy.request.scheme, hostaddr, hostport, fkey)
                else:
                    absfilepath = 'http://%s/file/%s/%s' % (hostaddr, fkey, filename.split(os.path.sep)[-1])
                    delurl = 'http://%s/upload/delete?key=%s' % (hostaddr, fkey)
                jnode = {'name':absfilepath,'size':size,'url':absfilepath, 'delete_url':delurl, 'delete_type':'DELETE'}
                jobj.append(jnode)
            conn.close()
            return json.dumps(jobj).decode()       
    get.exposed = True 
    
    def do(self, myFile, key):
        if not (cherrypy.session.get('login') == True) and not (cherrypy.session.get('ip') == cherrypy.request.remote.ip):
            raise cherrypy.HTTPRedirect(["/login/"], 302)
        myFile.filename = myFile.filename.replace('"', '').replace("'", '')
        if ':' in myFile.filename:
            myFile.filename = myFile.filename.replace('/',os.path.sep).split(os.path.sep)[-1]
        #cherrypy.log.error("FileName: " + myFile.filename)
        relpath = key + os.path.sep + myFile.filename.replace('/',os.path.sep)
        #cherrypy.log.error("RELPATH:  " + relpath)
        fpath = get_upload_path() + relpath
        froot = '/#'
        if '\\' in relpath:
            froot = get_upload_path() + os.path.sep + key + os.path.sep + myFile.filename.split('/')[0]
            pathparts = relpath.split('\\')
            newpath = get_upload_path()
            #cherrypy.log.error("FROOT:  " + froot)
            for i in range(0, len(pathparts)-1):
                #cherrypy.log.error("PRE MKDIR:  " + newpath + pathparts[i] + '\\')
                newpath = newpath + pathparts[i] +'\\'
                if  not os.path.exists(newpath):
                    #cherrypy.log.error("MKDIR:  " + newpath)
                    os.mkdir(newpath)
        mkey = key
        
        if fpath[-1] == '.':
            conn = sqlite3.connect(settings['db_name'])
            rkey = db.query_filekey(mkey, conn)
            if not rkey:
                rkey = db.insert_file(froot, cherrypy.session.get('user'), conn, mkey, mkey)
            else:
                conn.close()
            conn = sqlite3.connect(settings['db_name'])
            key = db.insert_file(fpath[0:-2], cherrypy.session.get('user'), conn, rkey)
            #cherrypy.log.error("FOLDER:: KEY: "+key+"\r\n+MKEY: "+mkey+"\r\nRKEY: "+rkey)
            
            hostaddr = cherrypy.request.local.ip
            hostport = cherrypy.request.local.port
        
            if hostaddr == '': 
                hostaddr = 'localhost'
            #print hostaddr 
            if hostport != 80:
                absfilepath = '%s://%s:%s/file/%s/%s' % (cherrypy.request.scheme, hostaddr, hostport, key, myFile.filename)
                delurl = '%s://%s:%s/upload/delete?key=%s' % (cherrypy.request.scheme, hostaddr, hostport, key)
            else:
                absfilepath = 'http://%s/file/%s/%s' % (hostaddr, key, myFile.filename)
                delurl = 'http://%s/upload/delete?key=%s' % (hostaddr, key)
            rpath = 'http://%s/file/%s' % (hostaddr, mkey)
        
            jobj = [{'name':'Folder: '+myFile.filename[0:-1],'size':myFile.length,'url':absfilepath,'rpath':rpath,'delete_url':delurl, 'delete_type':'DELETE'}]
            #return render(title="Upload complete",content="""<h2>Upload Complete!</h2><br>
            #                                                <div style="padding-left:15px;">The url for your file is:<br> %s</div>""" % absfilepath)
            return json.dumps(jobj).decode()
            
        #cherrypy.log.error(fpath)
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
            data = myFile.file.read(4092)
            if not data:
                break
            f.write(data)
            size += len(data)
        f.close()
        

        froot = get_upload_path() + os.path.sep + key
        conn = sqlite3.connect(settings['db_name'])
        rkey = db.query_filekey(mkey, conn)
        if not rkey:
            rkey = db.insert_file(froot, cherrypy.session.get('user'), conn, mkey, mkey)
        else:
            conn.close()
            
        #cherrypy.log.error("FILE:: KEY: "+key+"\r\nMKEY: "+mkey+"\r\nRKEY: "+rkey)
            
        conn = sqlite3.connect(settings['db_name'])
        key = db.insert_file(fpath, cherrypy.session.get('user'), conn, mkey)   
             
        hostaddr = cherrypy.request.local.ip
        hostport = cherrypy.request.local.port
    
        if hostaddr == '': 
            hostaddr = hostaddr = settings['hostname']#'localhost'
        #print hostaddr 
        if hostport != 80:
            absfilepath = '%s://%s:%s/file/%s/%s' % (cherrypy.request.scheme, hostaddr, hostport, key, myFile.filename)
            delurl = '%s://%s:%s/upload/delete?key=%s' % (cherrypy.request.scheme, hostaddr, hostport, key)
        else:
            absfilepath = 'http://%s/file/%s/%s' % (hostaddr, key, myFile.filename)
            delurl = 'http://%s/upload/delete?key=%s' % (hostaddr, key)
        rpath = 'http://%s/file/%s' % (hostaddr, mkey)
        jobj = [{'name':absfilepath,'size':myFile.length,'url':absfilepath,'rpath':rpath, 'delete_url':delurl, 'delete_type':'DELETE'}]
        #return render(title="Upload complete",content="""<h2>Upload Complete!</h2><br>
        #                                                <div style="padding-left:15px;">The url for your file is:<br> %s</div>""" % absfilepath)
        return json.dumps(jobj).decode()
    do.exposed = True 
      
    def delete(self, key):
        if not (cherrypy.session.get('login') == True) and not (cherrypy.session.get('ip') == cherrypy.request.remote.ip):
            raise cherrypy.HTTPRedirect(["/login/"], 302)
        if cherrypy.request.method == 'DELETE':
            #cherrypy.log.error("In delete")
            import shutil
            conn = sqlite3.connect(settings['db_name'])
            filename = db.query_filekey(key, conn)
            #cherrypy.log.error(filename)
            if filename:
                if os.path.isdir(filename):
                    try:
                        shutil.rmtree(filename)
                    except:
                        shutil.rmtree(filename)
                else:
                    try:
                        os.remove(filename)
                    except:
                        db.delete_filekey(key, conn)
                        return 'File/Folder does not exist'.decode()
                db.delete_filekey(key, conn)
                conn.commit()
                conn.close()
                return 'Delete Successful'.decode()
            return 'No file in database'.decode()
        return 'HTTP Method Error'.decode()
    delete.exposed = True
    
#=============================================================================
#  [
# {
#  "name":"picture1.jpg",
#  "size":902604,
#  "url":"\/\/example.org\/files\/picture1.jpg",
#  "thumbnail_url":"\/\/example.org\/thumbnails\/picture1.jpg",
#  "delete_url":"\/\/example.org\/upload-handler?file=picture1.jpg",
#  "delete_type":"DELETE"
# },
#   ]
#=============================================================================