from CDGRD.settings.base import *

DEBUG = True

ALLOWED_HOSTS = ['carloshdelreal.pythonanywhere.com']


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'carloshdelreal$consejeria',
        'USER': 'carloshdelreal',
        'PASSWORD': 'geologia2014',
        'HOST': 'carloshdelreal.mysql.pythonanywhere-services.com',
        'OPTIONS': {
        'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
