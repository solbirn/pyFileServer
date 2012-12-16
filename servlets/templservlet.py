#!/usr/bin/env python
# -*- coding: utf-8
from templates import base

def import_settings(path='pfs.conf'):
    settings = {}
    with open(path) as fHandle:
        linenum = 1
        for line in fHandle:
            setting = line.strip().split('#')[0].split('=')
            try:
                if setting[0] == '' or setting[1] == '':
                    linenum+=1
                    continue
                settings.update({setting[0]:setting[1]})
            except IndexError:
                print 'A line in the config file is not properly formatted:\n--Line %d: %s' % (linenum, line)
            linenum+=1
    if not settings.has_key('ip'):
        setting.update({'ip':'127.0.0.1'})
    if not settings.has_key('port'):
        setting.update({'port':80})
    else:
        settings['port'] = int(settings['port'])
    if not settings.has_key('db_name'):
        print 'Database name empty: Assuming database name is "pfsdb".'
        settings.update({'db_name':'pfsdb'})
    if not settings.has_key('db_type'):
        settings.update({'db_type':'sqlite'})
        print 'Using SQLite as Database server.'
    else:
        if settings['db_type'] == 'mysql':
            print 'Using MySQL as Database server.'
            if not settings.has_key('db_username'):
                print 'MySQL username missing. Fix and try again.'
                sys.exit(1) 
            if not settings.has_key('db_password'):
                print 'MySQL password missing. Fix and try again.'
                sys.exit(1) 
            if not settings.has_key('db_host'):
                print 'MySQL host ip/name missing. Fix and try again.'
                sys.exit(1)
            if not settings.has_key('db_port'):
                print 'MySQL port number missing. Fix and try again.'
                sys.exit(1)
            else: settings['db_port'] = int(settings['db_port'])
    if not settings.has_key('upload_dir'):
        import os
        if os.name == 'nt':
            settings.update({'upload_dir':os.path.expandvars("%USERPROFILE%\\Downloads\\")})
        else:
            settings.update({'upload_dir':os.path.expandvars("$HOME/Downloads/")})
    else:
        import os
        settings['upload_dir'] = os.path.expandvars(settings['upload_dir'])
    if not settings.has_key('serve_dir'):
        settings.update({'serve_dir':False})
    else:
        if settings['serve_dir'] == '0' or settings['serve_dir'].lower() == 'false':
            settings['serve_dir'] = False
        elif settings['serve_dir'] == '1' or settings['serve_dir'].lower() == 'true':
            settings['serve_dir'] = True
    if not settings.has_key('hostname'):
        settings.update({'hostname':'localhost'})
    return settings

__settings__ = import_settings()
__templ__ = {
             '__server_info__':'File-Keys v0.4'
             }

def render(type='htmldoc',title="Untitled", content=None, login=False):
    if login:
        logintxt = '<a href="/logout">Logout</a>'
    else:
        logintxt = '<a href="/login">Login</a>'
    if type == 'htmldoc':
        templ = base.base(searchList=[{'title':title,'content':content,'hostname':__settings__['hostname'],'loginout':logintxt}])
        mainMethod = getattr(templ, '_mainCheetahMethod_for_%s' % templ.__class__.__name__)
        return getattr(templ, mainMethod)()
    else: return __templ__[type]
