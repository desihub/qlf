Changing Desispec Version
===========================

Desispec is a submodule in QLF and it's version can be changed inside it's diretory

::

    qlf
    └── backend
        └── desispec

From there it's possible to make changes and checkout to other git version.


::

    ~/qlf/backend/desispec$ git status
    HEAD detached at 10d1c39
    nothing to commit, working directory clean

After the changes are made run ``./restartBackend`` to restart the containers with the latest code.

::

    ~/qlf$ ./restartBackend.sh
    Stopping qlf_app_1 ... done
    Recreating 9c38c1b6436a_qlf_db_1    ... done
    Recreating ac0c3d755824_qlf_redis_1 ... done
    Recreating qlf_app_1                ... done
    Recreating qlf_nginx_1              ... done

.. _map-code-inside-container:

Map Code Inside Container
--------------------------

Make sure the volumes are mapped inside the container to make the changes.

*docker-compose.yml* example:

.. code-block:: docker
   :emphasize-lines: 6,7

   ...
   app:
       build: ./backend
       env_file:
       - ./backend/global-env
       volumes:
       - ./backend/:/app
   ...