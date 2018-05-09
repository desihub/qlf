## DESI Quick Look Framework

The Quick Look Framework (QLF) is part of the DES Instrument Control System (ICS) and provides an interface to execute the Quick Look (QL) pipeline and display data quality information in realtime. 

QLF current version allows to follow the execution of QL pipeline, which process multiple cameras/arms in parallel. The interfaces for QA display are now in a mature stage of development using React and Bokeh plots.

_Requires ~2 GB_

### Install Docker

We use Docker as a container to install QLF. Install `docker` and `docker-compose` from the links below:

- [docker](https://docs.docker.com/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

_Make sure `docker --version`, `docker-compose --version`, and `docker ps` runs without error._

### Clone Quick Look Framework Project

    git clone https://github.com/desihub/qlf.git
    
_Everything you need is contained in this repository. Even `desispec` and `desiutil` as sub-repositories._

### Install default qlf configuration

Get into `qlf` directory and configure it. 

    cd qlf
    ./configure.sh

_Besides setting the environment and cloning desispec and desiutil, this downloads the [data](http://portal.nersc.gov/project/desi/data/quicklook/20190101_small.tar.gz) used for tests (~1 GB)._

### Starting QLF

Start QLF frontend and backend.

    ./start.sh

### User Interface

You can access QLF interface by going to 

    http://localhost:3000/

### Stoping QLF

    ./stop.sh

## FAQ

- If you are using linux and got this error:

```
ubuntu ~/docker $ docker-compose up -d
ERROR: Couldn't connect to Docker daemon at http+docker://localunixsocket - is it running?

If it's at a non-standard location, specify the URL with the DOCKER_HOST environment variable.
```

Add your current user to docker group:

`sudo usermod -aG docker $USER`

And make sure to log out of your terminal prompt and log back in in order for `usermod` change to take effect.

- If port is already allocated

For instance,
``` 
ERROR: for db  Cannot start service db: driver failed programming external connectivity on endpoint backend_db_1 (4d2adece087f3df9a3e34695246a22db6639e63e8b8054e3cb03f1209252b88d): Bind for 0.0.0.0:5433 failed: port is already allocated
```

Run `docker ps` to check for old containers up and running on your machine.

```
$ docker ps
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                                                                NAMES
17c6cef9f994        redis               "docker-entrypoint.s…"   23 hours ago        Up 23 hours         0.0.0.0:6380->6379/tcp                                                               backend_redis_1
9d93b1511b31        frontend_frontend   "sh entrypoint.sh"       23 hours ago        Up 23 hours         0.0.0.0:3000->3000/tcp                                                               frontend_frontend_1
00a5ff89d32d        qlf_qlf             "/usr/bin/tini -- ./…"   3 weeks ago         Up 7 days           0.0.0.0:5007->5007/tcp, 0.0.0.0:8001->8001/tcp, 0.0.0.0:56006->56006/tcp, 8000/tcp   qlf_qlf_1
d0cd726fc527        postgres            "docker-entrypoint.s…"   5 weeks ago         Up 7 days           0.0.0.0:5433->5432/tcp 
```

You can stop it individually by name, for example: `docker stop qlf_qlf_1`

- In case you need to access the backend

    http://localhost:8001/


### Support


    Contact: helpdesk@linea.gov.br
