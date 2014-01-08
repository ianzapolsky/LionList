import os,sys

apache_configuration = os.path.dirname(__file__)
project = os.path.dirname(apache_configuration)
workspace = os.path.dirname(project)
sys.path.append(workspace)
sys.path.append('/django/lionlist')
sys.path.append('/django')

os.environ['DJANGO_SETTINGS_MODULE'] = 'lionlist.settings.aws'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
