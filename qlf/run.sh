#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run QLF in development mode, create db if it does not exist
# start QLF web application and QLF daemon

# Test user for the development db
export TEST_USER=nobody
export TEST_USER_EMAIL=${TEST_USER}@example.com
export TEST_USER_PASSWD=nobody

# Initialize the development database for the first time
DEVDB="db.sqlite3"

if [ ! -f $DEVDB ];
then
    # Create the development database
    python manage.py makemigrations
    python manage.py migrate

    # Create superuser for Django admin interface
    # The password created here is used to access de admin interface and the browsable API
    echo "For development use password: $TEST_USER_PASSWD"
    python manage.py createsuperuser --username $TEST_USER --email $TEST_USER_EMAIL

fi

echo "Remember to start the bokeh server in another terminal..."

sleep 1

# Start QLF daemon
# python bin/qlf.py &

# Start QLF REST API
python manage.py runserver





