#!/bin/bash
if [ $UPDATE_DEPENDENCIES = "True" ]; then
	conda install -y --file requirements.txt
	pip install -r extras.txt
fi

export LANG=en_US.UTF-8  
export LANGUAGE=en_US:en  
export LC_ALL=en_US.UTF-8

export QLF_PROJECT=$(pwd)/framework/qlf
export QLF_ROOT=$(pwd)

for package in desispec desiutil desimodel desisim desitarget specter speclite; do
  echo "Setting $package..."
  export PATH=$QLF_ROOT/$package/bin:$PATH
  export PYTHONPATH=$QLF_ROOT/$package/py:$PYTHONPATH
done

export PYTHONPATH=$QLF_ROOT/framework/bin:$PYTHONPATH
export DESIMODEL=$QLF_ROOT/desimodel

if [ $START_ICS = "True" ]; then
  # Staring ics interface
  sh $QLF_ROOT/ics.sh
  if [ $LOGS_DIRECTORY = "True" ]; then
    python3.6 $QLF_ROOT/framework/bin/ics_daemon.py &> $QLF_ROOT/logs/ics_interface.log &
  else
    python3.6 $QLF_ROOT/framework/bin/ics_daemon.py &
  fi 
fi

if [ ! -z $POSTGRES_PASSWORD_FILE ]; then
  # Set db password nersc
  export POSTGRES_PASSWORD=$(cat $POSTGRES_PASSWORD_FILE)
fi

if [ $RUN_DB_MIGRATIONS = "True" ]; then
  python -Wi framework/qlf/manage.py migrate
  echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass') if not User.objects.all() else None" | python framework/qlf/manage.py shell
fi

# Start QLF daemon
if [ $DAEMON_TEST = "False" ]; then
  echo "Initializing QLF Daemon..."
  if [ $LOGS_DIRECTORY = "True" ]; then
    ./startDaemon.sh &> $QLF_ROOT/logs/qlf_daemon.log &
  else
    ./startDaemon.sh &
  fi 
fi

echo -e "\n\n\n----------------------------------------------------------------------"
echo "Initializing QLF Backend..."
echo -e "----------------------------------------------------------------------\n\n\n"

if [ $LOGS_DIRECTORY = "True" ]; then
  bokeh serve --allow-websocket-origin $BOKEH_HOST --num-procs 0 framework/qlf/dashboard/bokeh/timeseries/timeseries.py framework/qlf/dashboard/bokeh/regression/regression.py &> $QLF_ROOT/logs/bokeh.log &
  python -u $QLF_PROJECT/manage.py runserver 0.0.0.0:$QLF_PORT &> $QLF_ROOT/logs/runserver.log
else
  bokeh serve --allow-websocket-origin $BOKEH_HOST --num-procs 0 framework/qlf/dashboard/bokeh/timeseries/timeseries.py framework/qlf/dashboard/bokeh/regression/regression.py &
  python -u $QLF_PROJECT/manage.py runserver 0.0.0.0:$QLF_PORT
fi
