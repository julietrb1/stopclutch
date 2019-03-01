import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = '!*8(_j2!%+nb14fd(4r+k-*&0t3e19hxh@dr=#tvl1x^4in$sy'
DEBUG = True
ALLOWED_HOSTS = ['*']
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'stopclutch',
        'USER': 'stopclutch',
        'PASSWORD': 'stopclutch',
        'HOST': 'localhost',
        'PORT': '',
    }
}
