source /software/products/eups-2.1.4/bin/setups.sh 
setup DOSlib
setup QLFInterface

export QLF_ROOT=$(pwd)

export PYTHONPATH=$QLF_ROOT/framework/bin:$PYTHONPATH

python -Wi $QLF_ROOT/framework/bin/ics_daemon.py
