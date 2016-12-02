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

``DOSlib`` API will provide methods to query the opsDB, for example ``DOSlib.get_last_expid()`` returns information about the last observed exposure such as ``expid``, ``obsdate`` and
``flavor`` and ``DOSlib.get_files(expid)`` can be used to transfer the required input files from DOS (or from the DOS test environment)
to QLF local disk:

 - Exposure (a FITS file with 30 HDUs one per camera)
 - Calibration files (Fiber flat, PSF Boot, etc)

NOTE: Exposure metadata, telemetry data, fibermap and ETC data will also be obtained from opsDB using ``DOSlib``.


QL Framework
------------

Orchestrates the execution of the QL pipeline and store relevant QA results in the database for visualization.

The QLF database keeps information about the execution, and QA measurements associated with a given camera and
exposure.

    .. figure:: _static/qlfdb.png
       :name: qlfdb
       :target: _static/qlfdb.png
       :alt: QLF v0.2 database

       Figure 2. Schema of the QLF v0.2 database


QA metrics are pre-loaded into the ``QAMetric`` table as part of the database initialization. A QA metric has just ``name``, ``description``, and ``unit``.

1. Call ``DOSlib.get_last_expid()``

2. If last observed ``expid`` > last processed ``expid``; then call ``QLF.register(exposure)``. The exposure registration inserts just the ``expid``, ``obsdate`` and ``flavor`` in the ``Exposure`` table.

NOTE: we want to register all exposures regardless of the ``flavor``, this information is useful for night statistics but only `object` exposures will be
processed

3. If ``flavor`` is `object`; then call ``DOSlib.get_files(expid)``

4. Ingest exposure metadata (available in the FITS header at this point)

NOTE: can be done in item 2 too, depending whether we want metadata for non `object` exposures or not.

5. Split the exposure and fiberflat files in individual FITS files (one for each camera) and call ``QLF.register(camera)`` which fills the ``Camera`` table.

NOTE: other inputs are needed (e.g fibermap, PSF boot, etc)

5. Generate the QL configuration (one file for each camera) based on the current saved configuration

NOTE: The QL configuration can be changed on-the-fly via the interface

7. Execute 30 instances of the QL pipeline (one for each camera) in parallel

8. During the execution of each instance, each processing step makes an HTTP post to fill the ``Measurement`` table with the corresponding QA output, associated with the current exposure and camera (async)

NOTE: we need the QA results as soon as they are produced in order to monitor the execution in real-time; we can't wait the end of the pipeline
execution in order to ingest the results. The partial results of each step for each camera must be
available immediately for visualization. For each exposure that means about 10 QAs x 30 cameras HTTP requests, which should be fine.

Discuss failure recovery.

9. Go back to 1.

NOTE: For dark time the exposure time (900s) > than the processing time, but for bright time the exposure time
will be shorter than the processing time. Note that the above algorithm works for both, we always process the most recent
exposure.

A typical HTTP POST in the QLF API looks like:

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

Implemented independently, it is launched by QLF. QL pipeline communicates back with the QLF framework via HTTP POST.

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

