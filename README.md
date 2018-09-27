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
    
_Everything you need is contained in this repository. Even `desimodel`, `desisim`, `desitarget`, `desispec` and `desiutil` as sub-repositories._

### Install default qlf configuration

Get into `qlf` directory and configure it. 

_Make sure you have [svn](https://subversion.apache.org/packages.html) installed_

    cd qlf
    ./configure.sh

_Besides setting the environment and cloning desispec and desiutil, this downloads the [data](http://portal.nersc.gov/project/desi/data/quicklook/20190101_small.tar.gz) used for tests (~1 GB)._

### Starting QLF

Start QLF frontend and backend.

    ./start.sh

_frontend takes about 5 minutes to start on dev mode_

#### Making sure all containers are up

Running `docker ps` you should see 4 containers:

```
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                    NAMES
d92b7eb3583e        qlf_nginx           "nginx -g 'daemon of…"   5 minutes ago       Up 5 minutes        80/tcp, 7070/tcp, 0.0.0.0:80->8080/tcp   qlf_nginx_1
7622ffe8f2a9        qlf_backend         "/usr/bin/tini -- ./…"   5 minutes ago       Up 5 minutes        8000/tcp                                 qlf_backend_1
1c69cb7e5aff        redis               "docker-entrypoint.s…"   5 minutes ago       Up 5 minutes        6379/tcp                                 qlf_redis_1
709cc22755bc        postgres            "docker-entrypoint.s…"   5 minutes ago       Up 5 minutes        5432/tcp                                 qlf_db_1
```

### User Interface

You can access QLF interface by going to 

    http://localhost/

### Stoping QLF

    ./stop.sh

### Restarting QLF backend to update desispec changes

    ./restartBackend.sh

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
CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                    NAMES
d92b7eb3583e        qlf_nginx           "nginx -g 'daemon of…"   5 minutes ago       Up 5 minutes        80/tcp, 7070/tcp, 0.0.0.0:80->8080/tcp   qlf_nginx_1
7622ffe8f2a9        qlf_backend         "/usr/bin/tini -- ./…"   5 minutes ago       Up 5 minutes        8000/tcp                                 qlf_backend_1
1c69cb7e5aff        redis               "docker-entrypoint.s…"   5 minutes ago       Up 5 minutes        6379/tcp                                 qlf_redis_1
709cc22755bc        postgres            "docker-entrypoint.s…"   5 minutes ago       Up 5 minutes        5432/tcp                                 qlf_db_1
```

You can stop it individually by name, for example: `docker stop qlf_qlf_1`

- In case you need to access the backend

    http://localhost/dashboard/api/


### Support


    Contact: helpdesk@linea.gov.br
