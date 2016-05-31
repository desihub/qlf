# Specific settings for production
#
# Set the environment variable DJANGO_SETTINGS_MODULE to
# 'squash.settings.production' in order to use this file, for example:
#
# export DJANGO_SETTINGS_MODULE=qlf.settings.production

from . import defaults

# WARNING: the following parameters are no suitable for production yet
# See https://docs.djangoproject.com/en/1.8/howto/deployment/checklist/

DEBUG = False
