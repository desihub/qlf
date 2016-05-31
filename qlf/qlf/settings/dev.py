# Specific settings for development

from .defaults import *

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

BOKEH_URL='http://localhost:5006'
