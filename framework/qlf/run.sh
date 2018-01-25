#!/bin/bash

export QLF_PROJECT=$(pwd)

# Run QLF in development mode, create db if it does not exist
# start QLF web applicationi, Bokeh server and the QLF daemon

export PYTHONPATH=$PYTHONPATH:$(pwd)

if [ "$QLF_ROOT" == "" ];
then
	echo "Set QLF_ROOT environment variable first. In a default QLF installation, you should run:"
	echo "export QLF_ROOT=$HOME/quicklook"
	exit 1
fi

if [ "$(conda info -e | grep "*" | cut -d " " -f1)" != "quicklook" ];
then
    echo "Set quicklook conda environment first. In a default QLF installation, you should run:"
    echo "source ~/miniconda3/bin/activate quicklook"
    exit 1
fi

cd $QLF_PROJECT

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

python -Wi manage.py migrate > /dev/null
python -Wi manage.py createsuperuser --noinput --username $TEST_USER --email $TEST_USER_EMAIL

# Start QLF web application

if [ -f $QLF_ROOT/run.pgid ]; then
    RUN_PGID=`cat $QLF_ROOT/run.pgid`
    ps opgid | grep $RUN_PGID > /dev/null && echo "Another instance of QLF is running, terminating..."; kill -- -$RUN_PGID > /dev/null
fi

# Start django and bokeh servers and save the process group id

echo "Starting QLF..."
echo "Setting DESI Quick Look environment..."

for package in desispec desiutil; do
	echo "Setting $package..."
	export PATH=$QLF_ROOT/$package/bin:$PATH
	export PYTHONPATH=$QLF_ROOT/$package/py:$PYTHONPATH
done

nohup python -Wi manage.py runserver > $QLF_ROOT/runserver.log 2>&1 & echo $(ps opgid= $!) > $QLF_ROOT/run.pgid
nohup bokeh serve --allow-websocket-origin=localhost:8000 dashboard/bokeh/qasnr dashboard/bokeh/monitor dashboard/bokeh/exposures dashboard/bokeh/footprint > $QLF_ROOT/bokeh.log 2>&1 &

echo "QLF web application is running at http://localhost:8000 you may start Quick Look from the pipeline interface."

# Clean previous log

logfile=$(grep logfile ../config/qlf.cfg | cut -f2 -d=)
echo > $logfile

echo "QLF is running, watch $logfile" 

# Start QLF daemon
nohup python -Wi ../bin/qlf_daemon.py > $QLF_ROOT/qlf_daemon.log 2>&1 &
