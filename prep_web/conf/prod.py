from .common import *
import os
import json

with open('/etc/pconfig.json')as config_file:
        config = json.load(config_file)

with open('/etc/dbpassword.txt') as f:
    DB_PASSWORD = f.read().strip()

SECRET_KEY = config['SECRET_KEY']
ALLOWED_HOSTS = ['10.49.0.136','127.0.0.1','prep.moh.gov.jm','www.prep.moh.gov.jm']

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}




