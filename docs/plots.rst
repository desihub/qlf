Bokeh Plots
============

All `QA plots`_ are located at:

.. _`QA plots`: https://github.com/desihub/qlf/tree/master/backend/framework/qlf/dashboard/bokeh

::

    qlf
    └── backend
        └── framework
            └── qlf
                └── dashboard
                    └── bokeh
                        ├── qacheckarc
                        ├── qacheckflat
                        ├── qacountbins
                        ├── qacountpix
                        ├── qagetbias
                        ├── qainteg
                        ├── qaskycont
                        ├── qaskypeak
                        ├── qaskyR
                        ├── qasnr
                        ├── qaxwsigma
                        ├── qaxyshifts
                        └── plots

* Each directory has a ``main.py`` file containing QA plots logic. To make new plots inside the QA they are the only place that will require changes.

* ``Plots`` diretory contains commonly used functions throughout QAs.

* Changes saved will trigger a bokeh reloaded automatically if the code is correctly mapped inse the container (:ref:`map-code-inside-container`).

* `Jupyter examples`_

.. _`Jupyter examples`: https://github.com/desihub/qlf/tree/master/jupyter

In order to understand how the plots end up in the frontend there are also `3 files`_ divided by ``Flavor`` mapping each python QA to the appropriate frontend stage and name.

.. _`3 files`: https://github.com/desihub/qlf/tree/master/backend/framework/ql_mapping

::

    qlf
    └── backend
        └── framework
            └── ql_mapping
                ├── arc.json
                ├── flat.json
                └── science.json

They also exist in the `frontend directory`_.

.. _`frontend directory`: https://github.com/desihub/qlf/tree/master/frontend/src/assets/ql_mapping

::

    qlf
    └── frontend
        └── src
            └── assets
                └── ql_mapping
                    ├── arc.json
                    ├── flat.json
                    └── science.json

They are used to help mapping important keys and log messages used during the pipeline monitoring.

*Unless new QAs are added or changes are made in desispec keys and messages monitored by QLF there is no need to edit this files.*
