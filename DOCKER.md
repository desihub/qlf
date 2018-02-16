# Install Docker

- [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/)

_Make sure `docker --version`, `docker-compose --version` and `docker ps` runs without error._

# Running locally with docker

### Config file.
This file sets which cameras and exposures will be processed

`cp framework/config/qlf.cfg.template framework/config/qlf.cfg`

### Test data for local run of QLF: night 20190101, exposures 3 and 4.

```
mkdir spectro && cd spectro
wget -c http://portal.nersc.gov/project/desi/data/quicklook/20190101_small.tar.gz 
```

_IF using OSX and wget not available, download with curl -O_

### Unzip

```
tar xvzf 20190101_small.tar.gz
rm 20190101_small.tar.gz
```

## Starting QLF

    docker-compose up

## Stoping QLF

    docker-compose stop

OR

    docker ps
    docker stop REDIS_NAME
    docker stop QLF_NAME

_usually `docker stop qlf_qlf_1` and `docker stop qlf_redis_1`_

## Starting Pipeline

    http://localhost:8000/start
