Using docker and docker-compose
================================

This is not a comprehensive guide on how to use docker and all of it's features but will give you common used commands.

List Running Containers
--------------------------------
::

    $ docker ps
    CONTAINER ID        IMAGE               COMMAND             CREATED             STATUS              PORTS               NAMES

Build containers:
--------------------------------

::

    docker-compose build

*To build a specific container*

::

    docker-compose build NAME

*e.g.* ``docker-compose build nginx``

Start a container
--------------------------------

::

    $ docker-compose up

*Start in background*: ``docker-compose up -d``
*Start specific container*: ``docker-compose up -d NAME``

Stop all containers
--------------------------------

::

    docker-compose stop

Stop and delete containers
--------------------------------

This will delete the container but not the built images. This is usually used for puging database entries.

::

    docker-compose down

Delete all images from machine
--------------------------------

This will delete all images, containers, volumes and networks created. Usually used to clean environment.

::

    docker system prune -a

Work from inside the container
--------------------------------

You can work from inside the container. This is useful to check if the correct versions are being used.

.. code-block:: docker
   :emphasize-lines: 7

    ~/qlf/docs$ docker ps
    CONTAINER ID        IMAGE                                                    COMMAND                  CREATED             STATUS              PORTS                                            NAMES
    46d12dd9e9ef        qlf_nginx                                                "nginx -g 'daemon of…"   24 minutes ago      Up 24 minutes       80/tcp, 0.0.0.0:80->8080/tcp                     qlf_nginx_1
    29ff55378420        linea/qlf:BACK6f9165e25b07d92782cb2a7ab341ea013da99ac3   "/usr/bin/tini -- ./…"   24 minutes ago      Up 24 minutes       0.0.0.0:5006->5006/tcp, 0.0.0.0:8000->8000/tcp   qlf_app_1
    f1d141fa6f50        postgres                                                 "docker-entrypoint.s…"   24 minutes ago      Up 24 minutes       5432/tcp                                         qlf_db_1
    3ae98699a50f        redis                                                    "docker-entrypoint.s…"   24 minutes ago      Up 24 minutes       6379/tcp                                         qlf_redis_1
    ~/qlf/docs$ docker exec -it qlf_app_1 bash
    root@29ff55378420:/app#

.. _restart-backend:

Restart Backend
----------------

After the changes are made in the backend run ``./restartBackend`` to restart the containers with the latest code if it doesn't do it automatically.

::

    ~/qlf$ ./restartBackend.sh
    Stopping qlf_app_1 ... done
    Recreating 9c38c1b6436a_qlf_db_1    ... done
    Recreating ac0c3d755824_qlf_redis_1 ... done
    Recreating qlf_app_1                ... done
    Recreating qlf_nginx_1              ... done

FAQ
-------

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

Run ``docker ps`` to check for old containers up and running on your machine.

::

    $ docker ps
    CONTAINER ID        IMAGE               COMMAND                  CREATED             STATUS              PORTS                                    NAMES
    d92b7eb3583e        qlf_nginx           "nginx -g 'daemon of…"   5 minutes ago       Up 5 minutes        80/tcp, 7070/tcp, 0.0.0.0:80->8080/tcp   qlf_nginx_1
    7622ffe8f2a9        qlf_backend         "/usr/bin/tini -- ./…"   5 minutes ago       Up 5 minutes        8000/tcp                                 qlf_backend_1
    1c69cb7e5aff        redis               "docker-entrypoint.s…"   5 minutes ago       Up 5 minutes        6379/tcp                                 qlf_redis_1
    709cc22755bc        postgres            "docker-entrypoint.s…"   5 minutes ago       Up 5 minutes        5432/tcp                                 qlf_db_1


You can stop it individually by name, for example: ``docker stop qlf_qlf_1``