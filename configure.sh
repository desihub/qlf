#!/bin/sh
echo 'Cloning desispec and desiutil'
git submodule init
git submodule update

echo 'Copying qlf.cfg default settings to backend/framework/config/qlf.cfg'
cd backend
cp framework/config/qlf.cfg.template framework/config/qlf.cfg

echo 'Copying default backend docker-compose.yml'
cp docker-compose.yml.template docker-compose.yml

echo 'Copying default frontend docker-compose.yml'
cd ..
cd frontend
cp docker-compose.yml.template docker-compose.yml

echo 'Copying default frontend .env'
cp .env.template .env

cd ..
echo 'Checking spectro test data'
if [ "$(ls -A backend/spectro/data)" ]; then
    echo "=> spectro test data check OK"
else
    echo 'Downloading spectro test data'
    cd backend
    mkdir spectro && cd spectro
    wget -c http://portal.nersc.gov/project/desi/data/quicklook/20190101_small.tar.gz 

    echo 'Unzipping...'
    tar xvzf 20190101_small.tar.gz
    rm 20190101_small.tar.gz
fi

echo 'To start run ./start.sh'