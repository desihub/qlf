import os

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
    'debug_toolbar'
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
)

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
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

BOKEH_URL='http://{}:{}'.format(
    os.environ.get('BOKEH_SERVER', HOSTNAME),
    os.environ.get('BOKEH_PORT', '5006')
)

QLF_DAEMON_URL='PYRO:{}@{}:{}'.format(
    os.environ.get('QLF_DAEMON_NS', 'qlf.daemon'),
    os.environ.get('QLF_DAEMON_HOST', HOSTNAME),
    str(os.environ.get('QLF_DAEMON_PORT', 56005))
)

QLF_MANUAL_URL='PYRO:{}@{}:{}'.format(
    os.environ.get('QLF_MANUAL_NS', 'qlf.manual'),
    os.environ.get('QLF_DAEMON_HOST', HOSTNAME),
    str(os.environ.get('QLF_DAEMON_PORT', 56005))
)