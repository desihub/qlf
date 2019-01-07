#!/bin/bash
export LANG=en_US.UTF-8  
export LANGUAGE=en_US:en  
export LC_ALL=en_US.UTF-8

export QLF_PROJECT=/app/backend/framework/qlf
export QLF_ROOT=/app/backend/

export DESI_ROOT=$QLF_ROOT
export DESI_PRODUCT_ROOT=$QLF_ROOT

for package in desispec desiutil desimodel desisim desitarget specter speclite; do
  echo "Setting $package..."
  export PATH=$QLF_ROOT/$package/bin:$PATH
  export PYTHONPATH=$QLF_ROOT/$package/py:$PYTHONPATH
done

export PYTHONPATH=$QLF_ROOT/framework/bin:$PYTHONPATH
export DESIMODEL=$QLF_ROOT/desimodel

jupyter notebook --ip=0.0.0.0