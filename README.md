## DESI Quick Look Framework

The Quick Look Framework (QLF) is part of the DES Instrument Control System (ICS) and provides an interface to execute the Quick Look (QL) pipeline and display data quality information in realtime. 

QLF current version allows to follow the execution of QL pipeline, which process multiple cameras/arms in parallel. The interfaces for QA display are now in a mature stage of development using React and Bokeh plots.

_Requires ~5 GB_

### Install Docker

- [docker](https://docs.docker.com/install/) and [docker-compose](https://docs.docker.com/compose/install/)

_Make sure `docker --version`, `docker-compose --version` and `docker ps` runs without error._

### Clone Quick Look Framework Project

    git clone https://github.com/desihub/qlf.git

### Install default qlf configuration

    cd qlf
    ./configure.sh

### Starting QLF

    ./start.sh

### User Interface

    http://localhost:3000/

### API backend

    http://localhost:8001/

### Stoping QLF

    ./stop.sh

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


### Support


    Contact: helpdesk@linea.gov.br
