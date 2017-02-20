Quick Look Framework
====================

.. toctree::
   :maxdepth: 2

Angelo Fausti, Luiz da Costa, Rafael Silva and `LIneA <http://www.linea.gov.br>`_ team.

.. note::
    QLF v0.2 work in progress.

Introduction
^^^^^^^^^^^^

The Quick Look Framework (QLF) will display QA metrics computed by the DESI Quick Look (QL) pipeline and will provide feedback to the
observers about the quality of the data in real-time. QLF must interface the Data Online System (DOS) to get input files and metadata
required to run QL.

This document describes QLF v0.2, an early version of the standalone QLF. The standalone
QLF is meant to run locally and emulate the interface with the DESI Data Online System (DOS)
and execute the QL pipeline. The QA results are ingested into a database and displayed in a dashboard
interface accessible through the browser.

.. hint::

    See the `README <https://github.com/linea-it/qlf/blob/master/README.md>`_ for instructions on how to clone the repository,
    install the dependencies and run QLF locally.

QLF components
^^^^^^^^^^^^^^

Figure 1 shows the main components of QLF.

    .. figure:: _static/qlf.png
       :name: qlf
       :target: _static/qlf.png
       :alt: QLF components

       Figure 1. QLF components.


DOS emulator
------------

Emulates the acquisition of new exposures. DOS emulator main goal is to enable to run Quick Look
locally on a controlled cadence in order to test the framework.  It also can anticipate aspects of the QLF interface with the "real" DOS.


DOS Monitor
-----------

Implements the interface with DOS (or DOS emulator) to access the input files and metadata required to run the QL pipeline.

A DOS API called ``DOSlib`` will provide methods to query the DESI operations database (opsDB), for example ``DOSlib.get_last_expid()``
will return information about the last observed exposure such as ``expid``, ``obsdate`` and
``flavor`` and all other metadata we want to ingest in the QLF exposure table; ``DOSlib.get_files()`` returns URLs (or paths)
from DOS so that the required files to execute QL pipeline can be transferred to the local disk. We assume a exposure will be a single FITS file with 30 HDUs (one per camera).

.. note::
    we need to specify similar methods for calibration files (fiber flat, psf boot, etc), telemetry, fibermap and ETC data.
    We assume they also can be obtained from DOS using the ``DOSlib`` API.


Quick Look wrapper
------------------

Its final goal is to orchestrate the execution of the QL pipeline on the 30 CCDs in parallel and ingests the QA results into the QLF database.

For QLF v0.2 we are running the QL pipeline on a single CCD and with a fixed configuration based on ``desispec 0.11.0``.

QA results are uploaded to the QLF database by the QL pipeline using the ``qlf_ingest`` python module as they are
produced.

There is also a command line tool `bin/qlf_ingest.py <https://github.com/linea-it/qlf/tree/master/qlf/bin/qlf_ingest.py>`_
which has been used during development to populate the QLF database with QA results.


.. code:: bash

    $ python qlf_ingest.py --help
    usage: qlf_ingest.py [-h] --file FILE --qa-name QA_NAME [--force]

    Upload QA results produced by the Quick Look pipeline to QLF database.
    This script is meant to be run from the command line or imported by Quick Look.

    optional arguments:
      -h, --help         show this help message and exit
      --file FILE        Path to QA file produced by Quick Look
      --qa-name QA_NAME  Name of the QA metric to be ingested
      --force            Overwrite QA results for a given metric


.. hint::

    Use the following command to load a local file with QA results produced by the QL pipeline into the QLF database
    for display:

    .. code:: bash

        $ cd qlf/bin
        $ python qlf_ingest.py --qa-name SNR --file ../test/data/qa-snr-r0-00000000.yaml


QLF database
------------

The QA results associated with a given camera, exposure as well as QL execution information
are store in the QLF database.

    .. figure:: _static/qlfdb.png
       :name: qlfdb
       :target: _static/qlfdb.png
       :alt: QLF v0.2 database

       Figure 2. Schema of the QLF v0.2 database

The content of the database is exposed to the QLF dashboard through a REST API.


    .. hint::
        if you are running QLF locally you should be able to access `localhost:8000/dashboard/api/qa <http://localhost:8000/dashboard/api/qa>`_, this API
        endpoint shows the QA results that feed the dashboard interface.

        You can also filter by a specific QA and return the content as JSON
        `localhost:8000/dashboard/api/qa/?name=SNR&format=json <http://localhost:8000/dashboard/api/qa/?name=SNR&format=json>`_


QLF Dashboard
-------------

The QLF dashboard is the primary user interface (UI). The UI is composed by independend `Bokeh <http://bokeh.pydata.org/en/latest/>`_ apps located
at `dashboard/bokeh <https://github.com/linea-it/qlf/tree/master/qlf/dashboard/bokeh>`_.

The bokeh apps are grouped by an umbrella application based on the `ExtJS <http://examples.sencha.com/extjs/6.0.2/examples/kitchensink/#all>`_ library.

The bokeh apps are the building blocks for the QA visualization.
The `drill down` capability (not demonstrated in the current version yet) is possible by connecting the bokeh apps through their URLs and using URL parameters to control aspects
of data access and visualization.

    .. hint::
        The bokeh apps can be accessed individually at `localhost:5006 <http://localhost:5006>`_.

While Bokeh enables the QLF developer or the DESI scientist to create interactive visualization in Python,
the ExtJS is used to develop more complex interfaces, like the configuration interface (see below)


The dashboard will have different bokeh for QA visualization, monitoring the QL execution and configuring the QL pipeline.

Mock up of these interfaces are shown below


  .. figure:: _static/monitor.png
       :name: monitor
       :target: _static/monitor.png
       :alt: Mock up of the QLF monitor interface

       Figure 3. Mock up of the QLF monitor interface

  .. figure:: _static/exposures.png
       :name: exposures.png
       :target: _static/exposures.png
       :alt: Mock up of the interface for displaying QA results at the exposure level

       Figure 4. Mock up of the interface for displaying QA results at the exposure level

  .. figure:: _static/reports.png
       :name: reports.png
       :target: _static/reports.png
       :alt: Mock up of the interface for displaying QA nightly reports

       Figure 5. Mock up of the interface for displaying QA nightly reports


Configuration interface
-----------------------

The configuration interface uses some features provided by ``ExtJS`` library like the validation of the input parameters from
the interface. The graphical interface which represents the QL pipeline is specified as a JSON file containing the pipeline tasks and
the configuration options of each task.

The current implementation supports the following input fields: `Text field`, `Number field`, `Bollean field`, `Date field`,
`Single and Multiple choices`.

The current specification for the QL pipeline is here `static/ql.json <https://github.com/linea-it/qlf/blob/master/qlf/static/ql.json>`_

That specification is used to create the interface and is also used the generate the actual QL configuration file based on the user inputs.

  .. figure:: _static/config.png
       :name: config.png
       :target: _static/config.png
       :alt: Interface for managing the QL pipeline configuration

       Figure 5. Interface for managing the QL pipeline configuration



QLF execution (pseudo-code)
^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following reflects the current thinking for the QLF execution and will evolve as our understanding
of the system interfaces improve.

1. Call ``exposure = DOSlib.get_last_expid(params)``, it returns a JSON with the list of parameters specified in the argument
for the last observed exposure, those are the metadata we want to ingest in the ``Exposure Table``.

2. If ``expid`` > last processed ``expid``; then call ``qlf_ingest.post(exposure)``. The exposure registration inserts
the exposure object in the ``Exposure`` table.

.. note::
    we want to register all exposures regardless of its flavor (object, calibration, etc), this information is useful
    for night statistics but only `object` exposures are going to be processed by the QL pipeline.

.. note::
    at this point we could also fill the ``Camera`` table so that we have a ``camera_id`` for all the cameras that should
    be present. Alternatively the ``Camera`` table can be filled when registering the QA results.

3. If ``exposure['flavor']`` is `object`; then call ``DOSlib.get_files(expid)``

4. Transfer files to QLF local disk, for example using ``rsync``:

    .. code-block:: python

        remote_files = DOSlib.get_files(expid)
        for file in remote_files:
            cmd = ['rsync', '--ignore-existing', os.environ['USER']+'@'+file, data_dir]
            p = subprocess.call(cmd)

5. Split the exposure and fiber flat files in individual FITS files (one for each camera)

.. note::
    other inputs are needed at this point? e.g. for fibermap file we could used a method like ``DOSlib.get_fibermap(expid, spectrograph)`` that generates the input file required by QL pipeline.

6. Generate the QL configuration (one file for each camera) based on the current saved configuration in the QLF database.

.. note::
    the QL configuration can be changed on-the-fly via the interface, the new configuration will apply for the next exposure
    to be processed.

.. note::
    the ``Jobs`` table will changed in the schema, we need a job associated to each camera, so that we have individual execution times, individual logs, and status for each camera.


7. Execute 30 instances of the QL pipeline (one for each camera) in parallel


8. During the execution of each instance, each processing step uploads the QA results to QLF using the ``qlf_ingest.post()`` method.
This fills the ``QA`` table with the corresponding QA results associated to the current exposure and camera. For a given exposure
each camera will have several QA results produced at the different steps of the pipeline.

.. note::
    the partial QA results from each processing step and for each camera must be upload as soon as they are available
    for real-time visualization.


.. note::
    discuss failure recovery, discuss QL heartbeat.

9. Go back to 1.

.. note::
    for dark time, the exposure time (900s) > than the processing time.

    for bright time, the exposure time will be shorter than the processing time, in this case the above algorithm works
    because we always process the most recent exposure.

QL pipeline
-----------

Implemented independently by the SMU team. The QL pipeline is launched by QLF.

The processing steps and associated QAs are listed below:

1. Preprocessing:

 - https://github.com/desihub/desidatamodel/blob/master/doc/QUICKLOOK/qa-countpix-CAMERA-EXPID.rst
 - https://github.com/desihub/desidatamodel/blob/master/doc/QUICKLOOK/qa-getbias-CAMERA-EXPID.rst
 - https://github.com/desihub/desidatamodel/blob/master/doc/QUICKLOOK/qa-getrms-CAMERA-EXPID.rst
 - https://github.com/desihub/desidatamodel/blob/master/doc/QUICKLOOK/qa-xwsigma-CAMERA-EXPID.rst

2. Extraction: desispec.boxcar.py

 - https://github.com/desihub/desidatamodel/blob/master/doc/QUICKLOOK/qa-countbins-CAMERA-EXPID.rst


3. Fiber Flattening: desispec.quickfiberflat.py

 - https://github.com/desihub/desidatamodel/blob/master/doc/QUICKLOOK/qa-integ-CAMERA-EXPID.rst
 - https://github.com/desihub/desidatamodel/blob/master/doc/QUICKLOOK/qa-skycont-CAMERA-EXPID.rst
 - https://github.com/desihub/desidatamodel/blob/master/doc/QUICKLOOK/qa-skypeak-CAMERA-EXPID.rst

4. Sky Subtraction: desispec.quicksky.py

 - https://github.com/desihub/desidatamodel/blob/master/doc/QUICKLOOK/qa-snr-CAMERA-EXPID.rs


Schedule
^^^^^^^^

The gantt chart below shows QLF milestones according to the SOW between DESI and LIneA. "light blue" corresponds to the ICS
milestone (WBS 1.7.10), "dark blue" to the Survey QA Interface milestones (WBS 1.8.3.8) and "yellow"
correspond to testing/feedback from the DESI collaboration.

During QLF development, subtasks in each milestone will be detailed.

.. raw:: html

    <IFRAME WIDTH=1000 HEIGHT=700 FRAMEBORDER=0 SRC="https://app.smartsheet.com/b/publish?EQBCT=3a74696141d64da795cf3d8923142558"></IFRAME>

Overview of the functionalities to be implemented in each milestone, intermediate versions are planned.

 - Demonstrator (v0.1): demonstration of QLF technology stack and main concepts. In this initial version QLF produces a scalar metric (e.g. median SNR), stores its value in the database and display the result in a web page. The selected technologies prioritize the use of Python as the main development language. The application uses `Django <https://www.djangoproject.com/>`_ and the `Bokeh <http://bokeh.pydata.org/en/latest/>`_ python plotting library to create interactive visualizations in the browser.

 - Early QLF (v0.2): QLF interface to control the pipeline execution and display the execution logs; new database schema including ``Exposure`` and ``Camera`` tables; ingestion of QA outputs as JSON blobs in the ``QA`` table. Include at least one example of interactive plot  (e.g SNR vs. mag)

 - Intermediate QLF (v0.5): Add more QA plots. Configuration interface. DOS emulator. Moniroting Interface. Start thinking about processing the 30 CCDs. Preparation for the first mock observing tests.

 - Production QLF (v1.0): Production ready, second round of mock observing tests.

References
==========

*TODO*

* :ref:`search`

