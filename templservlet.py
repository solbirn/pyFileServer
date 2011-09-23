from settingsservlet import import_settings
from templates import base

__settings__ = import_settings()

__templ__ = {
             '__server_info__':'PyFileServer 0.02'
             }

def render(type='htmldoc',title="Untitled", content=None):
    if type == 'htmldoc':
        templ = base.base(searchList=[{'title':title,'content':content,'hostname':__settings__['hostname']}])
        mainMethod = getattr(templ, '_mainCheetahMethod_for_%s' % templ.__class__.__name__)
        return getattr(templ, mainMethod)()
    else: return __templ__[type]
