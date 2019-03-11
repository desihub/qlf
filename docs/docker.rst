Install Docker
================================================

We use Docker as a container to install QLF. Install `docker` and `docker-compose` from the links below:

- `docker`_
- `docker-compose`_

.. _docker: https://docs.docker.com/install/
.. _docker-compose: https://docs.docker.com/compose/install/

Make sure ``docker --version``, ``docker-compose --version``, and ``docker ps`` runs without error.

This is not a comprehensive guide on how to use docker and all of it's features but will give you common used commands.

Using Docker and docker-compose
--------------------------------

1. Listing running containers

::

    $ docker ps
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

2. Build containers:

::

    docker-compose build

*To build a specific container*

::

    docker-compose build NAME

*e.g.* ``docker-compose build nginx``

3. Start a container

::

    $ docker-compose up

*Start in background*: ``docker-compose up -d``

4. Stop all containers

::

    docker-compose stop

5. Stop and delete containers

This will delete the container but not the built images. This is usually used for puging database entries.

::

    docker-compose down

6. Delete all images from machine

This will delete all images, containers, volumes and networks created. Usually used to clean environment.

::

    docker system prune -a

FAQ
------------------------------

1. If you are using linux and got this error:

::

    ubuntu ~/docker $ docker-compose up -d
    ERROR: Couldn't connect to Docker daemon at http+docker://localunixsocket - is it running?

    If it's at a non-standard location, specify the URL with the DOCKER_HOST environment variable.

Add your current user to docker group:

::

    sudo usermod -aG docker $USER

And make sure to log out of your terminal prompt and log back in in order for ``usermod`` changes take effect.

2. If port is already allocated

For instance,

::

    ERROR: for db  Cannot start service db: driver failed programming external connectivity on endpoint backend_db_1 (4d2adece087f3df9a3e34695246a22db6639e63e8b8054e3cb03f1209252b88d): Bind for 0.0.0.0:5433 failed: port is already allocated

Run `docker ps` to check for old containers up and running on your machine.

::

    $ docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                    NAMES
    d92b7eb3583e        qlf_nginx           "nginx -g 'daemon of…"   5 minutes ago       Up 5 minutes        80/tcp, 7070/tcp, 0.0.0.0:80->8080/tcp   qlf_nginx_1
    7622ffe8f2a9        qlf_backend         "/usr/bin/tini -- ./…"   5 minutes ago       Up 5 minutes        8000/tcp                                 qlf_backend_1
    1c69cb7e5aff        redis               "docker-entrypoint.s…"   5 minutes ago       Up 5 minutes        6379/tcp                                 qlf_redis_1
    709cc22755bc        postgres            "docker-entrypoint.s…"   5 minutes ago       Up 5 minutes        5432/tcp                                 qlf_db_1


You can stop it individually by name, for example: ``docker stop qlf_qlf_1``