#!/bin/bash

if [ $UPDATE_DEPENDENCIES = "true" ]; then
	conda install -y --file requirements.txt
	pip install -r extras.txt
fi

export LANG=en_US.UTF-8  
export LANGUAGE=en_US:en  
export LC_ALL=en_US.UTF-8

export QLF_PROJECT=$(pwd)/framework/qlf
export QLF_ROOT=$(pwd)
export QLF_REDIS=True

export DESI_ROOT=$QLF_ROOT
export DESI_PRODUCT_ROOT=$QLF_ROOT

for package in desispec desiutil desimodel desisim desitarget specter; do
	echo "Setting $package..."
	export PATH=$QLF_ROOT/$package/bin:$PATH
	export PYTHONPATH=$QLF_ROOT/$package/py:$PYTHONPATH
done

export PYTHONPATH=$QLF_ROOT/framework/bin:$PYTHONPATH
export DESIMODEL=$QLF_ROOT/desimodel

python -Wi framework/qlf/manage.py migrate
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass') if not User.objects.all() else None" | python framework/qlf/manage.py shell

# Start QLF daemon
if [ $DAEMON_TEST = "false" ]; then
	echo "Initializing QLF Daemon..."
	./startDaemon.sh &> $QLF_ROOT/logs/qlf_daemon.log &
fi


if [ $BOKEH_TEST = "false" ]; then
	echo "Initializing Bokeh Server..."
	./startBokeh.sh &> $QLF_ROOT/logs/bokeh.log &
fi

echo "QLF web application is running at http://$QLF_HOSTNAME:$QLF_PORT you may start Quick Look from the pipeline interface."

python -u $QLF_PROJECT/manage.py runserver 0.0.0.0:$QLF_PORT &> $QLF_ROOT/logs/runserver.log
