#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)

# Run QLF in development mode, create db if it does not exist
# start QLF web applicationi, Bokeh server and the QLF daemon

# Test user for the development db
export TEST_USER=nobody
export TEST_USER_EMAIL=${TEST_USER}@example.com
export TEST_USER_PASSWD=nobody

# Initialize the development database 
DEVDB="db.sqlite3"

if [ -f $DEVDB ];
then
    rm $DEVDB
fi
python -Wi manage.py migrate

# Create django superuser 
# The password created here is used to access de admin interface and the browsable API
echo
echo "For development you might use a password like: $TEST_USER_PASSWD"
echo

python -Wi manage.py createsuperuser --username $TEST_USER --email $TEST_USER_EMAIL

echo "Starting QLF..." 
# QLF web application
python -Wi manage.py runserver &
# Bokeh server
bokeh serve --allow-websocket-origin=localhost:8000 dashboard/bokeh/qa-snr & 
# QLF daemon
python -Wi ../bin/qlf_daemon.py 
