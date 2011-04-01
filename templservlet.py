__templ__ = {
             'simple':"""<html><head><title>%s</title></head><body>%s</body></html>""",
             '__server_info__':'JCT File Server 0.02'
             }

__settings__ = {
                'uploaddir': {'windows':"%USERPROFILE%\\Downloads\\", 'posix':"$HOME/Downloads/"},
                'hostname': 'localhost',
                'servedir': False
                }

def render(type='simple'):
    return __templ__[type]