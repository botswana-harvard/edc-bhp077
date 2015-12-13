import os
import sys
#import site
#import platform

VIRTUALENV_PATH = '/home/django/.virtualenvs/django-1.6.7/'
SOURCE_ROOT_PATH = '/home/django/source/bhp077/'
LOCAL_PROJECT_RELPATH = 'microbiome/'

# Add the site-packages of the chosen virtualenv to work with
activate_env=os.path.join(VIRTUALENV_PATH, 'bin/activate_this.py')
execfile(activate_env, dict(__file__=activate_env))
# update path
sys.path.insert(0, os.path.join(VIRTUALENV_PATH, 'local/lib/python2.7/site-packages'))
sys.path.insert(0, os.path.join(SOURCE_ROOT_PATH, 'edc_project'))
sys.path.insert(0, os.path.join(SOURCE_ROOT_PATH, 'lis_project'))
sys.path.insert(0, os.path.join(SOURCE_ROOT_PATH, LOCAL_PROJECT_RELPATH))
os.environ['DJANGO_SETTINGS_MODULE'] = 'bhp077.settings'

# Activate the virtual env

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()