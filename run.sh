#!/bin/bash
source activate quicklook 

export QLF_PROJECT=$(pwd)/framework/qlf
export QLF_ROOT=$(pwd)

cd $QLF_ROOT/framework/bin/
echo "Initializing QLF Daemon..."

# Start QLF daemon
python -Wi qlf_daemon.py &
celery -A tasks worker --loglevel=info &

cd $QLF_PROJECT

echo "Initializing QLF database..."
# Test user for the development db
export TEST_USER=nobody
export TEST_USER_EMAIL=nobody@example.com
export TEST_USER_PASSWD=nobody

# Initialize the development database
DEVDB="db.sqlite3"
if [ -f $DEVDB ];
then
    rm $DEVDB
fi

python -Wi manage.py makemigrations
python -Wi manage.py migrate > /dev/null
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell

echo "QLF web application is running at http://$QLF_HOSTNAME:8000 you may start Quick Look from the pipeline interface."

bokeh serve --allow-websocket-origin=$QLF_HOSTNAME --allow-websocket-origin=$QLF_HOSTNAME:8000 --host=$QLF_HOSTNAME:5006 --port=5006 dashboard/bokeh/qasnr dashboard/bokeh/monitor dashboard/bokeh/exposures dashboard/bokeh/footprint &> $QLF_ROOT/bokeh.log &
python -u manage.py runserver 0.0.0.0:8000
