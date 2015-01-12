#!/home/dave/.virtualenvs/scgshort/bin/python
import sys, os

INTERP = "/home/dave/.virtualenvs/scgshort/bin/python"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)
  
sys.path.append(os.getcwd())
#sys.path.append(os.path.join(os.getcwd(), 'needle'))
sys.path.insert(0, '/home/dave/.virtualenvs/scgshort/bin')
#sys.path.insert(0, 'home/dave/.virtualenvs/needle/lib/python2.7/site-packages/django')
sys.path.insert(0, '/home/dave/.virtualenvs/scgshort/lib/python2.7/site-packages')
  

 
os.environ['DJANGO_SETTINGS_MODULE'] = "scgshort.settings"
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()

#from paste.exceptions.errormiddleware import ErrorMiddleware
#application = ErrorMiddleware(application, debug=True)

