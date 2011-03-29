__templ__ = {'simple':"""<html><head><title>%s</title></head><body>%s</body></html>"""}

def render(type='simple'):
    return __templ__[type]