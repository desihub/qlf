#!/bin/bash
source activate quicklook

apt-get install -y locales && locale-gen en_US.UTF-8

export LANG=en_US.UTF-8
export LANGUAGE=en_US:en
export LC_ALL=en_US.UTF-8

export QLF_PROJECT=$(pwd)/framework/qlf
export QLF_ROOT=$(pwd)

for package in desispec desiutil desimodel specter; do
        echo "Setting $package..."
        export PATH=$QLF_ROOT/$package/bin:$PATH
        export PYTHONPATH=$QLF_ROOT/$package/py:$PYTHONPATH
done

export DESI_SPECTRO_DATA=$QLF_ROOT/spectro/data
export DESI_SPECTRO_REDUX=$QLF_ROOT/spectro/redux
export QL_SPEC_DATA=$DESI_SPECTRO_DATA
export QL_SPEC_REDUX=$DESI_SPECTRO_REDUX

export PYTHONPATH=$QLF_ROOT/framework/bin:$PYTHONPATH
export DESIMODEL=$QLF_ROOT/desimodel

QLCONFIG= 
NIGHT=
EXPID=
CAMERAS=
#CAMERAS="b2 r1 r3 r9 z1 z4 z5 z9"

run_ql () {
    local CAMERA=$1
    desi_quicklook -i $QLCONFIG -n $NIGHT -c $CAMERA -e $EXPID &> run-$CAMERA.log
}

for CAMERA in $CAMERAS; do run_ql "$CAMERA" & done
