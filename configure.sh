#!/bin/sh

echo 'Cloning desispec and desiutil'
git submodule init
git submodule update
cd backend/desimodel
svn export https://desi.lbl.gov/svn/code/desimodel/trunk/data
cd ../..

echo 'Copying default docker-compose.yml'
cp docker-compose.yml.template docker-compose.yml

echo 'Copying default nginx-proxy'
cd nginx
cp nginx-proxy.conf.template nginx-proxy.conf
cd ..

echo 'Copying default frontend .env'
cd frontend
cp .env.template .env
cd ..

if [ -z "$1" ]; then
    echo 'Checking spectro test data'
    if [ "$(ls -A backend/spectro/data)" ]; then
        echo "=> spectro test data check OK"
    else
        export FILE_SPECTRO=spectro.v6.tar.gz
        echo 'Downloading spectro test data'
        cd backend
        wget -c ftp://srvdatatransfer.linea.gov.br/qlfdata/$FILE_SPECTRO

        echo 'Unzipping...'
        tar xvzf $FILE_SPECTRO
        rm $FILE_SPECTRO
    fi
fi

echo 'To start run ./start.sh'
