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
if [ -z $1 ]; then
    python framework/qlf/manage.py test dashboard --noinput
else
    pip install coverage
    coverage run --source='.' framework/qlf/manage.py test dashboard --noinput
    coverage report
fi
