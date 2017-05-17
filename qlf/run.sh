#!/bin/bash

# Run QLF in development mode, create db if it does not exist
# start QLF web applicationi, Bokeh server and the QLF daemon

export PYTHONPATH=$PYTHONPATH:$(pwd)

if [ "$QLF_ROOT" == "" ];
then
	echo "Set QLF_ROOT environment variable first. Example:"
	echo "export QLF_ROOT=$HOME/quicklook"
	exit 1
fi
echo "Setting DESI Quick Look environment..."

source deactivate
source activate quicklook

for package in desispec desiutil; do
	echo "Setting $package..."
	export PATH=$QLF_ROOT/$package/bin:$PATH
	export PYTHONPATH=$QLF_ROOT/$package/py:$PYTHONPATH
done

echo "Initializing QLF database..."
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
bokeh serve --allow-websocket-origin=localhost:8000 dashboard/bokeh/qasnr dashboard/bokeh/monitor dashboard/bokeh/exposures & 
# QLF daemon
python -Wi ../bin/qlf_daemon.py 
