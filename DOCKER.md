_Requires ~5 GB_

# Install Docker

- [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/)

_Make sure `docker --version`, `docker-compose --version` and `docker ps` runs without error._

# Running locally with docker

#### Config file (qlf/framework/config/qlf.cfg)

This file sets which cameras and exposures will be processed. `framework/config/qlf.cfg.template` provides a example processing exposures `3` and `4`, arms `b`, `r` and `z` and spectrographs `0` and `1`. 

To use this configuration make a copy of the template using the line bellow.

`cp framework/config/qlf.cfg.template framework/config/qlf.cfg`

Other possible configurations are commented inside this file.

#### Test data for local run of QLF: night 20190101, exposures 3 and 4. (~1 GB)

```
mkdir spectro && cd spectro
wget -c http://portal.nersc.gov/project/desi/data/quicklook/20190101_small.tar.gz 
```

_IF using OSX and wget not available, download with curl -O_

#### Unzip

```
tar xvzf 20190101_small.tar.gz
rm 20190101_small.tar.gz
```

#### Docker compose file

```
cd ..
cp docker-compose.yml.template docker-compose.yml
```

## Starting QLF

    docker-compose up

## Starting Pipeline

    http://localhost:8001/start

## Stoping Pipeline

    http://localhost:8001/stop

## Stoping QLF

    docker-compose stop

OR

    docker ps
    docker stop REDIS_NAME
    docker stop QLF_NAME
    docker stop DB_NAME

_usually `docker stop qlf_qlf_1`, `docker stop qlf_redis_1` and `docker stop qlf_db_1`_

## FAQ

1. If you are using linux and got this error:

```
ubuntu ~/docker $ docker-compose up -d
ERROR: Couldn't connect to Docker daemon at http+docker://localunixsocket - is it running?

If it's at a non-standard location, specify the URL with the DOCKER_HOST environment variable.
```

Add your current user to docker group:

`sudo usermod -aG docker $USER`

And make sure to log out of your terminal prompt and log back in in order for `usermod` change to take effect.
