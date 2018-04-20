#!/bin/bash
source activate quicklook 

conda install -y --file requirements.txt
pip install -r extras.txt

export QLF_PROJECT=$(pwd)/framework/qlf
export QLF_ROOT=$(pwd)
export QLF_REDIS=True

for package in desispec desiutil; do
	echo "Setting $package..."
	export PATH=$QLF_ROOT/$package/bin:$PATH
	export PYTHONPATH=$QLF_ROOT/$package/py:$PYTHONPATH
done

cd $QLF_ROOT
echo "Initializing QLF Daemon..."

# Start QLF daemon
python -Wi framework/bin/qlf_daemon.py &> $QLF_ROOT/qlf_daemon.log &

cd $QLF_PROJECT

python -Wi manage.py migrate
# echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'pass')" | python manage.py shell

echo "QLF web application is running at http://$QLF_HOSTNAME:$QLF_PORT you may start Quick Look from the pipeline interface."

if [ $BOKEH_TEST = "false" ]; then
	bokeh serve $BOKEH_CONFIGURATION --port=$BOKEH_PORT dashboard/bokeh/qacountpix dashboard/bokeh/qaskycont dashboard/bokeh/qacountbins dashboard/bokeh/qagetbias dashboard/bokeh/qagetrms dashboard/bokeh/qainteg dashboard/bokeh/qaskypeak dashboard/bokeh/qasnr dashboard/bokeh/qaskyresid dashboard/bokeh/qaxwsigma dashboard/bokeh/monitor dashboard/bokeh/exposures dashboard/bokeh/footprint &> $QLF_ROOT/bokeh.log &
fi
python -u manage.py runserver 0.0.0.0:$QLF_PORT &> $QLF_ROOT/runserver.log
