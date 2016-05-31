#!/bin/bash
# Run dashboard app in development mode

if [ "$DJANGO_SETTINGS_MODULE" = "qlf.settings.production" ];
then
    echo "Do not use this script in production mode."
    exit 1
fi
# Test user for the development database
export TEST_USER=$USER
export TEST_USER_EMAIL=${USER}@example.com

# Initialize the development database for the first time
DEVDB="db.sqlite3"

if [ ! -f $DEVDB ];
then
    # Create the development database
    python manage.py makemigrations
    python manage.py migrate

    # Create superuser for Django admin interface
    # The password created here is used to access de admin interface and the browsable API
    python manage.py createsuperuser --username $TEST_USER --email $TEST_USER_EMAIL

fi
python manage.py loaddata initial_data
python manage.py runserver



