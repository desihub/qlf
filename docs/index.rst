Quick Look Framework
====================

.. toctree::
   :maxdepth: 2

Angelo Fausti, Robson Goncalves, Luiz N. da Costa

.. note::
    Work in progress.

Introduction
^^^^^^^^^^^^

Quick Look Framework (QLF) is designed display QA metrics from the DESI Quick Look pipeline and provide
feedback to observers about the quality of the data in real-time.

In development mode, QLF runs locally and emulates the Data Online System (DOS) environment to get the input files and
metadata required to run the QL pipeline.

See the `README <https://github.com/linea-it/qlf/blob/master/README.md>`_ for instructions on how to clone the repository,
install the software dependencies and start QLF in development mode.

System Design
^^^^^^^^^^^^^

The main components of QLF are described below

    .. figure:: _static/qlf.png
       :name: qlf
       :target: _static/qlf.png
       :alt: QLF system components

       Figure 1. QLF system components.


DOS Test Environment
--------------------

Emulates the acquisition of new exposures for integration tests during development.


DOS Monitor
-----------

Implements the interface with DOS (or DOS test environment) to access the input files and metadata required to run the QL pipeline.

``DOSlib`` API will provide methods to query the opsDB, for example ``DOSlib.get_last_exposure(params)`` returns information about the last observed exposure such as ``expid``, ``obsdate`` and
``flavor`` and all other metadata we want to ingest in the `Exposure` table; ``DOSlib.get_file_location(expid)`` return URLs (or paths)
for the required input files from DOS (or DOS test environment) so that the exposures can be transferred to QLF local disk.
We assume a exposure is a single FITS file with 30 HDUs (one per camera).


.. note::
    specify similar methods for calibration files (fiber flat, psf boot, ect), telemetry data, fibermap and ETC data. They also can be obtained from opsDB using ``DOSlib``.


QL Framework
------------

Orchestrates the execution of the QL pipeline and store relevant QA results in a relational database for visualization.

The QLF database keeps information about the execution, and QA measurements associated with a given camera and
exposure.

    .. figure:: _static/qlfdb.png
       :name: qlfdb
       :target: _static/qlfdb.png
       :alt: QLF v0.2 database

       Figure 2. Schema of the QLF v0.2 database

QA metrics are pre-loaded into the ``QAMetric`` table as part of the database initialization. A QA metric has a ``name``, ``category``, ``description``, and ``unit``.

1. Call ``exposure = DOSlib.get_last_exposure(params)``, it returns a JSON with the ``params`` for the last observed exposure from opsDB, those are the metadata we need to ingest in the ``Exposure Table``.

2. If ``expid`` > last processed ``expid``; then call ``QLF.register(exposure)``. The exposure registration inserts the exposure object in the ``Exposure`` table.

.. note::
    we want to register all exposures regardless of its type (object, calibration, etc), this information is useful for night statistics but only `object` exposures are going to be processed.

.. note::
    at this point we could also fill the `Camera` so that we have a ``cameraId`` for all cameras that should be present

3. If ``exposure['flavor']`` is `object`; then call ``DOSlib.get_file_location(expid)``

4. Transfer exposure to QLF local disk, for example using ``rsync``:

    .. code-block:: python

        remote_file= DOSlib.get_file_locationg(expid)
        cmd = ['rsync', '--ignore-existing', os.environ['USER']+'@'+remote_file, data_dir]
        p = subprocess.call(cmd)

5. Split the exposure and fiber flat files in individual FITS files (one for each camera)

.. note::
    other inputs are needed at this point? e.g. for fibermap file we could used a method like ``DOSlib.get_fibermap(expid, spectrograph)`` that generates the input file required by QL pipeline.

6. Generate the QL configuration (one file for each camera) based on the current saved configuration

.. note::
    the QL configuration can be changed on-the-fly via the interface, the configuration is per exposure.

.. note::
    ``Jobs`` table must be changed in the schema, we need a job associated to each camera, so that we have individual execution times, individual logs, and status for each camera.

7. Execute 30 instances of the QL pipeline (one for each camera) in parallel

8. During the execution of each instance, each processing step sends the QA outputs to QLF via an HTTP POST (async) which fills the ``Measurement`` table with the corresponding QA outputs associated with the current exposure and camera (each camera can have several QA outputs)

.. note::
    we need the QA ouputs as soon as they are produced in order to monitor the execution in real-time; we can't wait the completion of the pipeline execution in order to ingest the results. The partial results of each step for each camera must be available immediately for visualization. For each exposure that means about 10 QAs x 30 cameras HTTP requests, which should be fine.

.. note::
    discuss failure recovery.

9. Go back to 1.

.. note::
    for dark time the exposure time (900s) > than the processing time, but for bright time the exposure time will be shorter than the processing time. Note that the above algorithm works for both, we always process the most recent exposure.

A typical HTTP POST to the QLF API looks like:

.. code-block:: python

    >>> import requests
    >>> response = requests.get('http://localhost:8000/dashboard/api/')
    >>> response.status_code
    200
    >>> api = response.json()
    >>> job = {
                 "id": 1,
                 "expid": 0,
                 "camera": "r0",
                 "status": 0,
                 "measurements": [
                     {
                         "metric": "SNR",
                         "value": <JSON object of the QA output>
                     }
                 ]
               }
    >>> response = requests.post(api['job'], json=job, auth=(TEST_USER, TEST_PASSWD))
    >>> response.status_code
    201


QL pipeline
-----------

Implemented independently. It is launched by QLF. QL pipeline communicates back with QLF via HTTP POST.

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


Visualization
-------------

Web pages for display the QA metrics.


Implementation phases
^^^^^^^^^^^^^^^^^^^^^

 - **QLF v0.1**: demonstration of QLF technology stack and main concepts. In this initial version QLF produces a scalar metric (e.g. Median SNR), stores this value in the database and display the result in a web page. The selected technologies prioritize the use of Python as the main development language, and a mature framework like Django. The web dashboard uses `Django <https://www.djangoproject.com/>`_ and the `Bokeh <http://bokeh.pydata.org/en/latest/>`_ python plotting library to create interactive visualizations in the browser.

 - **QLF v0.2**: improvements in the QLF interface to control the pipeline execution and display the execution log; new database schema including ``Exposure`` and ``Camera`` tables; ingestion of QA outputs as JSON blobs in the ``Measurements`` table. Include at least an example of interactive plot  (e.g SNR vs. mag)

 - **QLF V0.3**: ...



References
==========

*TODO*

* :ref:`search`

