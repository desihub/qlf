Quick Look Framework
====================

.. toctree::
   :maxdepth: 2

Angelo Fausti, Alisson Lanot, Luiz N. da Costa

.. note::
    Work in progress.

Introduction
^^^^^^^^^^^^

Quick Look Framework (QLF) is designed display QA metrics from the DESI Quick Look pipeline and provide
feedback to observers about the quality of the data in real-time.

In development mode, QLF runs locally and emulates the Data Online System (DOS) environment to get the input files and
metadata required to run the QL pipeline.

See the `README <https://github.com/linea-it/qlf/blob/master/README.md>`_ for instructions on how to clone the repository,
install the software dependencies and start the QLF demo.

System Design
^^^^^^^^^^^^^

The main components of QLF are described below

    .. figure:: _static/qlf.png
       :name: qlf
       :target: _static/qlf.png
       :alt: QLF system components

       Figure 1. QLF system components.


 - **DOS Test Environment**: Emulates DOS environment for integration tests during development;
 - **DOS Monitor**: implements the interface with DOS (or DOS test environment) to access the input files
   and metadata required to run the QL pipeline;
 - **QLF App**: orchestrates the execution of the QL pipeline, prepare input data and configuration, launches the QL pipeline and store relevant information in the QLF database for display in the dashoard;
 - **QL pipeline**: implemented independently of the QLF, QL pipeline communicates with the QLF framework
   through the QLF API;
 - **Dashboard**: web pages for display the QA metrics.


TODO: include description of the dataflow


Implementation phases
^^^^^^^^^^^^^^^^^^^^^

 - **QLF v0.1**: demonstration of QLF technology stack and main concepts. In this initial version QLF produces a scalar metric (e.g. Median SNR), stores this value and job information in the database and display the result in a web page.
 - **QLF v0.2**: improvements in the QLF interface to include configuration, monitor and control the pipeline execution
 - **QLF v0.3**: first integration with QL pipeline, using simulated data and processing one ccd, still display aggregated metrics but includes a first implementation of the DOS Test Environment.
 - **QLF v0.4**: support individual and aggregated metrics, implement single CCD display
 - **QLF V0.5**: ...

QLF v0.1
^^^^^^^^

This section describes QLF v0.1 implementation.

The selected technologies prioritize the use of Python
as the main development language, and a mature framework like Django making the system easy to extend for DESI developers.
The web dashboard uses `Django <https://www.djangoproject.com/>`_ and the `Bokeh <http://bokeh.pydata.org/en/latest/>`_ python plotting library to create interactive visualizations in the browser.


QLF database
------------

The QLF database keeps information about the QA metrics and pipeline execution.

    .. figure:: _static/qlfdb.png
       :name: qlfdb
       :target: _static/qlfdb.png
       :alt: QLF v0.1 database

       Figure 2. QLF v0.1 database, showing ``Job``, ``Metric`` and associated ``Measurement`` tables.


QA metrics are registered in the ``Metric`` table. A metric has ``name``, ``description``, ``condition``
and a ``threshold`` that can be used to trigger alerts.

In QLF v0.1,  this table stores just **summary information** (e.g. median SNR per ccd). We plan to extend the schema in QLF v0.4 to support
individual and aggregated measurements adding the ``Spectrograph``, ``Ccd`` and ``Fiber`` tables in the schema (e.g. SNR of each fiber
associated to a given CCD and spectrograph as well as median SNR per CCD or Spectrograph)

Each execution of the pipeline is registered in the ``Job`` table and has ``start``, ``end`` time and a ``status``.

In the current schema, each job can perform *N* measurements and each measurement is associated to a metric.


The Execution framework
-----------------------

In QLF v0.1, the execution framework is simply a daemon that launches an executable code (a placeholder for the actual QL pipeline).
The output of this code is registered into the QLF database through the QLF API.

A typical call to the QLF API looks like:

.. code-block:: python

    >>> import requests
    >>> response = requests.get('http://localhost:8000/dashboard/api/')
    >>> response.status_code
    200
    >>> api = response.json()
    >>> job = {
                 "name": "test",
                 "status": 0,
                 "measurements": [
                     {
                         "metric": "SNR",
                         "value": 1.0
                     }
                 ]
               }
    >>> response = requests.post(api['job'], json=job, auth=(TEST_USER, TEST_PASSWD))
    >>> response.status_code
    201

the QLF daemon is implemented in `bin/qlf.py <https://github.com/linea-it/qlf/blob/master/qlf/bin/qlf.py>`_. In v0.1 it
sends a constant *SNR=1.0* each 10s to the QLF API.

.. note::
   In development mode the API can be reached at http://localhost:8000/dashboard/api with user=nobody and password=nobody


Visualization
-------------

For QLF v0.1 we integrated the Django framework and the Bokeh python library. In order to demonstrate this integration we implemented a dashboard that lists QA metrics registered in the QLF database (e.g Median SNR) and present an interactive time series plot
showing the values measured by each execution of the QL pipeline. Once QLF is integrated with the QL pipeline and we have single CCD processing in place we plan
to extend the dashboard based on requirements from the collaboration.

A screenshot of the current dashboard interface is shown below:

    .. figure:: _static/dashboard.png
       :name: dashboard
       :target: _static/dashboard.png
       :alt: QLF v0.1 dashboard

       Figure 2. QLF v0.1 dashboard, listing QA netrics and a time series plot.


References
==========

*TODO*

* :ref:`search`

