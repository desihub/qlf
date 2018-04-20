#!/bin/bash
source activate quicklook 

export QLF_PROJECT=$(pwd)/framework/qlf
export QLF_ROOT=$(pwd)
export QLF_REDIS=True

for package in desispec desiutil; do
	echo "Setting $package..."
	export PATH=$QLF_ROOT/$package/bin:$PATH
	export PYTHONPATH=$QLF_ROOT/$package/py:$PYTHONPATH
done

cd /app/framework/qlf
bokeh serve $BOKEH_CONFIGURATION --port=$BOKEH_PORT dashboard/bokeh/qacountpix dashboard/bokeh/qaskycont dashboard/bokeh/qacountbins dashboard/bokeh/qagetbias dashboard/bokeh/qagetrms dashboard/bokeh/qainteg dashboard/bokeh/qaskypeak dashboard/bokeh/qasnr dashboard/bokeh/qaskyresid dashboard/bokeh/qaxwsigma dashboard/bokeh/monitor dashboard/bokeh/exposures dashboard/bokeh/footprint
