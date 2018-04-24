import os
import sys

HOSTNAME = os.environ.get('QLF_HOSTNAME', 'localhost')

BASE_DIR = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

SECRET_KEY = os.environ.get('SECRET_KEY', os.urandom(32))

ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', HOSTNAME).split(',')

SITE_PAGES_DIRECTORY = os.path.join(BASE_DIR, 'layouts')

# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'rest_framework.authtoken',
    'dashboard',
    'debug_toolbar',
    'channels',
    'ui_channel',
    'django_postgrespool',
    'corsheaders',
)

MIDDLEWARE_CLASSES = (
    'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'corsheaders.middleware.CorsMiddleware',  
)

CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

INTERNAL_IPS = '127.0.0.1'
ROOT_URLCONF = 'dashboard.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'dashboard/templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'qlf.wsgi.application'

# Internationalization
# https://docs.djangoproject.com/en/1.8/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.8/howto/static-files/

STATIC_URL = '/static/'

STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'static'),
    )

DEBUG = os.environ.get('DEBUG', 'True') == 'True'

# Database
# https://docs.djangoproject.com/en/1.8/ref/settings/#databases

DATABASES = {
    'default': {
        #'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'ENGINE': 'django_postgrespool',
        'NAME': os.environ.get('POSTGRES_DB', 'dbqlf'),
        'USER': os.environ.get('POSTGRES_USER', 'userqlf'),
        'PASSWORD': os.environ.get('POSTGRES_PASSWORD', 'qlfuser'),
        'HOST': os.environ.get('DB_NAME', 'db'),
        'PORT': '',
    }
}

if 'test' in sys.argv or 'test_coverage' in sys.argv:
    DATABASES['default']['ENGINE'] = 'django.db.backends.sqlite3'

DATABASE_POOL_ARGS = {
    'max_overflow': 30,
    'pool_size': 10
}

BOKEH_URL='http://{}:{}'.format(
    os.environ.get('BOKEH_SERVER', 'localhost'),
    os.environ.get('BOKEH_PORT', '5006')
)

QLF_DAEMON_URL='PYRO:{}@{}:{}'.format(
    os.environ.get('QLF_DAEMON_NS', 'qlf.daemon'),
    os.environ.get('QLF_DAEMON_HOST', 'localhost'),
    str(os.environ.get('QLF_DAEMON_PORT', 56005))
)

QLF_MANUAL_URL='PYRO:{}@{}:{}'.format(
    os.environ.get('QLF_MANUAL_NS', 'qlf.manual'),
    os.environ.get('QLF_DAEMON_HOST', 'localhost'),
    str(os.environ.get('QLF_DAEMON_PORT', 56005))
)

QLF_BASE_URL = os.environ.get('QLF_BASE_URL', 'http://localhost:8000')
if os.environ.get('QLF_REDIS', False):
    CHANNEL_LAYERS = {
        "default": {
            "BACKEND": "asgi_redis.RedisChannelLayer",
            "CONFIG": {
                "hosts": [(os.environ.get('REDIS_NAME', 'redis'), 6379)],
            },
            "ROUTING": "qlf.routing.channel_routing",
        },
    }

X_FRAME_OPTIONS = 'ALLOWALL'

XS_SHARING_ALLOWED_METHODS = ['POST','GET','OPTIONS', 'PUT', 'DELETE']

EMAIL_USE_TLS = os.environ.get('EMAIL_USE_TLS', None)
EMAIL_HOST = os.environ.get('EMAIL_HOST', 'localhost')
EMAIL_PORT = os.environ.get('EMAIL_PORT', 25)
