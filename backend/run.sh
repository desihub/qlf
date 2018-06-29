#!/bin/bash

# ./ics.sh

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

if [ $START_ICS = "true" ]; then
	# ICS Pyro configuration
	export PYRO_HOST=localhost
	export PYRO_REQUIRE_EXPOSE=False
	export PYRO_SERIALIZER=pickle
	export PYRO_THREADPOOL_SIZE=64
	export PYRO_PORT=56006
	export PYRO_SERIALIZERS_ACCEPTED=pickle

	# Staring ics interface
	sh $QLF_ROOT/ics.sh
	python3.6 $QLF_ROOT/framework/bin/ics_daemon.py &> $QLF_ROOT/logs/ics_interface.log &
fi

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
