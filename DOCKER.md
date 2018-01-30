### Install Docker

- [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/)

### Clone the Quick Look Framework Project

    git clone https://github.com/desihub/qlf.git
    cd qlf

### Running locally with docker

    # Config file.
    # This file sets which cameras and exposures will be processed

    cp framework/config/qlf.cfg.template framework/config/qlf.cfg

    # Test data for local run of QLF: night 20190101, exposures 3 and 4.

    mkdir spectro && cd spectro

    wget -c http://portal.nersc.gov/project/desi/data/quicklook/20190101_small.tar.gz 

    # IF using OSX and wget not available, download with curl -O

    # Unzip

    tar xvzf 20190101_small.tar.gz

    rm 20190101_small.tar.gz

### Starting QLF

    docker-compose up

### Stoping QLF

    docker-compose stop

### Starting Pipeline

    http://localhost:8000/start
