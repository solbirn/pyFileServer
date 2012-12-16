#!/usr/bin/env python
# -*- coding: utf-8



##################################################
## DEPENDENCIES
import sys
import os
import os.path
try:
    import builtins as builtin
except ImportError:
    import __builtin__ as builtin
from os.path import getmtime, exists
import time
import types
from Cheetah.Version import MinCompatibleVersion as RequiredCheetahVersion
from Cheetah.Version import MinCompatibleVersionTuple as RequiredCheetahVersionTuple
from Cheetah.Template import Template
from Cheetah.DummyTransaction import *
from Cheetah.NameMapper import NotFound, valueForName, valueFromSearchList, valueFromFrameOrSearchList
from Cheetah.CacheRegion import CacheRegion
import Cheetah.Filters as Filters
import Cheetah.ErrorCatchers as ErrorCatchers

##################################################
## MODULE CONSTANTS
VFFSL=valueFromFrameOrSearchList
VFSL=valueFromSearchList
VFN=valueForName
currentTime=time.time
__CHEETAH_version__ = '2.4.4'
__CHEETAH_versionTuple__ = (2, 4, 4, 'development', 0)
__CHEETAH_genTime__ = 1302113568.423
__CHEETAH_genTimestamp__ = 'Wed Apr 06 21:12:48 2011'
__CHEETAH_src__ = 'base.tmpl'
__CHEETAH_srcLastModified__ = 'Wed Apr 06 21:12:43 2011'
__CHEETAH_docstring__ = 'Autogenerated by Cheetah: The Python-Powered Template Engine'

if __CHEETAH_versionTuple__ < RequiredCheetahVersionTuple:
    raise AssertionError(
      'This template was compiled with Cheetah version'
      ' %s. Templates compiled before version %s must be recompiled.'%(
         __CHEETAH_version__, RequiredCheetahVersion))

##################################################
## CLASSES

class base(Template):

    ##################################################
    ## CHEETAH GENERATED METHODS


    def __init__(self, *args, **KWs):

        super(base, self).__init__(*args, **KWs)
        if not self._CHEETAH__instanceInitialized:
            cheetahKWArgs = {}
            allowedKWs = 'searchList namespaces filter filtersLib errorCatcher'.split()
            for k,v in KWs.items():
                if k in allowedKWs: cheetahKWArgs[k] = v
            self._initCheetahInstance(**cheetahKWArgs)
        

    def respond(self, trans=None):



        ## CHEETAH: main method generated for this template
        if (not trans and not self._CHEETAH__isBuffering and not callable(self.transaction)):
            trans = self.transaction # is None unless self.awake() was called
        if not trans:
            trans = DummyTransaction()
            _dummyTrans = True
        else: _dummyTrans = False
        write = trans.response().write
        SL = self._CHEETAH__searchList
        _filter = self._CHEETAH__currentFilter
        
        ########################################
        ## START - generated method body
        
        write(u'''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
<html xmlns="http://www.w3.org/1999/xhtml">
<head>
<meta http-equiv="Content-Type" content="text/html; charset=utf-8" />
<title>''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"title",True) # u'${title}' on line 5, col 8
        if _v is not None: write(_filter(_v, rawExpr=u'${title}')) # from line 5, col 8.
        write(u'''</title>
<style type="text/css">
<!--
body {
    font: 100%/1.4 Verdana, Arial, Helvetica, sans-serif;
    background: #4E5869;
    margin: 0;
    padding: 0;
    color: #000;
}

ul, ol, dl {
    padding: 0;
    margin: 0;
}
h1, h2, h3, h4, h5, h6, p {
    margin-top: 0;
    padding-right: 15px;
    padding-left: 15px;
}
a img { 
    border: none;
}
a:link {
    color:#414958;
    text-decoration: underline; 
}
a:visited {
    color: #4E5869;
    text-decoration: underline;
}
a:hover, a:active, a:focus { 
    text-decoration: none;
}

.outercontainer {
    width: 80%;
    max-width: 1260px;
    min-width: 780px;
    background: #FFF;
    margin: 0 auto;
}

.header {
    background: #6F7D94;
}

.sidebar1 {
    float: left;
    width: 20%;
    background: #93A5C4;
    padding-bottom: 10px;
}
.content {
    padding: 32px 0px;
    width: 65%;
    min-height:670px;
    float: left;
}
.sidebar2 {
    float: left;
    width: 20%;
    background: #93A5C4;
    padding: 10px 0;
}

.content ul, .content ol {
    padding: 0;
}

ul.nav {
    width: 100%;
    position: relative;
    list-style: none;
    list-style-type:none;
    /*border-top: 1px solid #666;
    border-bottom: 1px solid #666;*/
}
ul.nav li {
    float: left;
}
ul.nav a, ul.nav a:visited {
    padding: 5px 10px 5px 10px;
    display: block;
    text-decoration: none;
    background: #8090AB;
    color: #000;
}
ul.nav a:hover, ul.nav a:active, ul.nav a:focus {
    background: #6F7D94;
    color: #000;
}

.footer {
    padding: 10px 0;
    background: #6F7D94;
    position: relative;
    clear: both;
}

.fltrt {
    float: right;
    margin-left: 8px;
}
.fltlft {
    float: left;
    margin-right: 8px;
}
.clearfloat {
    clear:both;
    height:0;
    font-size: 1px;
    line-height: 0px;
}
.centered {
    padding-left: 25%;
    padding-right: 25%;
}
-->
</style><!--[if lte IE 7]>
<style>
.content { margin-right: -1px; } /* this 1px negative margin can be placed on any of the columns in this layout with the same corrective effect. */
ul.nav a { zoom: 1; }  /* the zoom property gives IE the hasLayout trigger it needs to correct extra whiltespace between the links */
</style>
<![endif]-->
<script src="/staticcache/js/jquery.min.js"></script>
<!-- Bootstrap CSS Toolkit styles -->
<link rel="stylesheet" href="/staticcache/css/bootstrap.min.css">
<!-- Generic page styles 
<link rel="stylesheet" href="/staticcache/css/style.css">-->
<!-- Bootstrap styles for responsive website layout, supporting different screen sizes -->
<link rel="stylesheet" href="/staticcache/css/bootstrap-responsive.min.css">
<!-- Bootstrap CSS fixes for IE6 -->
<!--[if lt IE 7]><link rel="stylesheet" href="/staticcache/css/bootstrap-ie6.min.css"><![endif]-->
<!-- Bootstrap Image Gallery styles -->
<link rel="stylesheet" href="/staticcache/css/bootstrap-image-gallery.min.css">
<!-- CSS to style the file input field as button and adjust the Bootstrap progress bars -->
<link rel="stylesheet" href="/staticcache/css/jquery.fileupload-ui.css">
<!-- Shim to make HTML5 elements usable in older Internet Explorer versions -->
<!--[if lt IE 9]><script src="/staticcache/js/html5.js"></script><![endif]-->
        <script type="text/javascript">
         function delete_key(key){
             $.ajax({
                  type: "DELETE",
                  url: "/upload/delete?key="+key
                });
            $("#"+key).fadeOut();
         };
         $(document).ready(function(){
             $('#batchname').change(function(){
             $.ajax({
                      type: "POST",
                      url: "/batches/change?key="+$('#key').val()+"&name="+$(this).val()
                    });
            });
        });
        </script>
        </head>

<body>

<div class="outercontainer" style="height:100%">
  <div class="header">
  <div >

  <div style="display:none"><a href="https://''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"hostname",True) # u'${hostname}' on line 129, col 39
        if _v is not None: write(_filter(_v, rawExpr=u'${hostname}')) # from line 129, col 39.
        write(u'''/"><img src="https://''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"hostname",True) # u'${hostname}' on line 129, col 70
        if _v is not None: write(_filter(_v, rawExpr=u'${hostname}')) # from line 129, col 70.
        write(u'''/" alt="Insert Logo Here" name="Logo" width="70" height="68" id="logo" /></a>
    </div>
    <div style="padding: 40px 20px 20px 20px;font-size:30px;vertical-align:bottom;line-height:10px">PFileServer<sup style="font-size:17px">BETA</sup><span style="padding-left:16px;padding-top:10px;font-size:15px;">Your key to simple, powerful, file sharing.™</span></div>
        
    </div>
        <div style="background: #8090AB; height: 28px;">
      <ul class="nav" style="background: #8090AB;">
          <li><a href="/batches">Batches</a></li>
          <li><a href="/upload">Upload</a></li>
          <li style="width:50%">
          <li style="float:right">''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"loginout",True) # u'${title}' on line 5, col 8
        if _v is not None: write(_filter(_v, rawExpr=u'${loginout}')) # from line 5, col 8.
        write(u'''</li>
    </ul></div>
    <!-- end .header -->
  </div>
  
  <div class="content" style="width:100%">
  ''')
        _v = VFSL([locals()]+SL+[globals(), builtin],"content",True) # u'${content}' on line 141, col 3
        if _v is not None: write(_filter(_v, rawExpr=u'${content}')) # from line 141, col 3.
        write(u'''
  <!-- end .content --></div>
  
  <div class="footer">
    <p></p>
    <!-- end .footer --></div>
  <!-- end .container --></div>
</body>
</html>''')
        
        ########################################
        ## END - generated method body
        
        return _dummyTrans and trans.response().getvalue() or ""
        
    ##################################################
    ## CHEETAH GENERATED ATTRIBUTES


    _CHEETAH__instanceInitialized = False

    _CHEETAH_version = __CHEETAH_version__

    _CHEETAH_versionTuple = __CHEETAH_versionTuple__

    _CHEETAH_genTime = __CHEETAH_genTime__

    _CHEETAH_genTimestamp = __CHEETAH_genTimestamp__

    _CHEETAH_src = __CHEETAH_src__

    _CHEETAH_srcLastModified = __CHEETAH_srcLastModified__

    _mainCheetahMethod_for_base= 'respond'

## END CLASS DEFINITION

if not hasattr(base, '_initCheetahAttributes'):
    templateAPIClass = getattr(base, '_CHEETAH_templateClass', Template)
    templateAPIClass._addCheetahPlumbingCodeToClass(base)


# CHEETAH was developed by Tavis Rudd and Mike Orr
# with code, advice and input from many other volunteers.
# For more information visit http://www.CheetahTemplate.org/

##################################################
## if run from command line:
if __name__ == '__main__':
    from Cheetah.TemplateCmdLineIface import CmdLineIface
    CmdLineIface(templateObj=base()).run()

