#!/bin/bash
echo "Initializing QLF Python..."
export LANG=en_US.UTF-8  
export LANGUAGE=en_US:en  
export LC_ALL=en_US.UTF-8

export QLF_ROOT=$(pwd)

for package in desispec desiutil desimodel desisim desitarget specter speclite; do
  echo "Setting $package..."
  export PATH=$QLF_ROOT/$package/bin:$PATH
  export PYTHONPATH=$QLF_ROOT/$package/py:$PYTHONPATH
done

export PYTHONPATH=$QLF_ROOT/framework/bin:$PYTHONPATH
export DESIMODEL=$QLF_ROOT/desimodel

python framework/qlf/manage.py shell --plain
