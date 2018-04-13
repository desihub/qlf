#!/bin/sh
echo 'Cloning desispec and desiutil'
cd backend
git submodule init
git submodule update

echo 'Copying qlf.cfg default settings to backend/framework/config/qlf.cfg'
cp framework/config/qlf.cfg.template framework/config/qlf.cfg

echo 'Downloading spectro test data'
mkdir spectro && cd spectro
wget -c http://portal.nersc.gov/project/desi/data/quicklook/20190101_small.tar.gz 

echo 'Unzipping...'
tar xvzf 20190101_small.tar.gz
rm 20190101_small.tar.gz

echo 'Copying default backend docker-compose.yml'
cd ..
cp docker-compose.yml.template docker-compose.yml

echo 'Copying default frontend docker-compose.yml'
cd ..
cd frontend
cp docker-compose.yml.template docker-compose.yml

echo 'Copying default frontend .env'
cp .env.template .env

echo 'To start run sh start.sh'