from .base import *

DEBUG = True

if(os.environ.get('MYSQL_ROOT_HOST', None) == None):
    FILE_NAME = 'export.sh'
    os.system('source../../export.sh')
    print('\n\n\n os.environ >>>>> ', os.environ)

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'HOST': os.environ['MYSQL_ROOT_HOST'],
        'NAME': os.environ['MYSQL_DATABASE'],
        'USER': os.environ['MYSQL_USER'],
        'PASSWORD': os.environ['MYSQL_ROOT_PASSWORD'],
        'PORT': 3306,
        'TEST': {
            'NAME': 'test_dooodb',
            'OPTIONS': {
                'charset': 'utf8',
            }
        },
    }
}