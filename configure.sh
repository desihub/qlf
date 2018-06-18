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

if [ -z "$1" ]; then
    cd ..
    echo 'Checking spectro test data'
    if [ "$(ls -A backend/spectro/data)" ]; then
        echo "=> spectro test data check OK"
    else
        export FILE_SPECTRO=spectro.v1.tar.gz
        echo 'Downloading spectro test data'
        cd backend
        wget -c ftp://srvdatatransfer.linea.gov.br/qlfdata/$FILE_SPECTRO

        echo 'Unzipping...'
        tar xvzf $FILE_SPECTRO
        rm $FILE_SPECTRO
    fi
fi

echo 'To start run ./start.sh'
