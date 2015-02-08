# Import from base.py, then override individual settings.
from .base import *

# Production values differ
DATABASES = {
     'default': {
         'ENGINE': 'django.db.backends.sqlite3',
         'NAME': os.path.join(BASE_DIR, '../../../database/db.sqlite3'),
     }
}
STATIC_ROOT = os.path.join(BASE_DIR, '../../../static')

DEBUG=False
ALLOWED_HOSTS=['ec2-54-154-168-49.eu-west-1.compute.amazonaws.com']
