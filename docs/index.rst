Quick Look Framework
====================

.. toctree::
   :maxdepth: 2

Angelo Fausti, Alisson Lanot, Luiz N. da Costa

.. note::
    Work in progress.

Introduction
^^^^^^^^^^^^

Quick Look Framework (QLF) is designed monitor QA outputs from the DESI Quick Look pipeline and provide
feedback to observers about the quality of the data in real-time.

In development mode, QLF runs locally emulating the Data Online System (DOS) environment to get the input files and
metadata required to run the QL pipeline.

See the `README <https://github.com/linea-it/qlf/blob/master/README.md>`_ for instructions on how to clone the repository, install the software dependencies and start the QLF demo.

System Design
^^^^^^^^^^^^^

The system components are shown below

    .. figure:: _static/qlf.png
       :name: qlf
       :target: _static/qlf.png
       :alt: QLF system components

       Figure 1. QLF system components.


 - **DOS Test Environment**: Emulates DOS enviroment for integration tests during development;
 - **DOS Monitor**: implements** the interface with DOS (or DOS test environment) to access the input files
   and metadata required to run the QL pipeline;
 - **QLF App**: orchestrates the execution of the QL pipeline, prepare input data and configuration, launches the QL pipeline and store relevant information in the QLF database for display in the dashoard;
 - **QL pipeline**: implemented independently of the QLF, QL pipeline communicates with the QLF framework
   through the QLF API;
 - **Dashboard**: web pages for the visualization of the results.


Implementation phases
^^^^^^^^^^^^^^^^^^^^^

 - **QLF v0.1**: demonstration of QLF technology stack and main concepts. In this initial version QLF produces a scalar metric (e.g. Median SNR), it stores this value and job information in the database and display the results in a web page.
 - **QLF v0.2**: first integration with QL pipeline, using simulated data and processing one ccd, still display aggregated metrics but includes a first implementation of the DOS Test Environment.
 - **QLF v0.3**: support individual and aggreatted metrics, implement single CCD display, display QL ouput logs in the dashboard
 - **QLF v0.4**: configuration and submission interface for QL
 - **QLF V0.5**: ...

QLF v0.1
^^^^^^^^

This section describes QLF v0.1 implementation.

The selected technologies prioritize the use of Python
as the main development language, and a mature framework like Django making the system easy to extend for DESI developers.
The web dashboard uses `Django <https://www.djangoproject.com/>`_ and the `Bokeh <http://bokeh.pydata.org/en/latest/>`_ python plotting library to create interactive visualizations in the browser.


QLF database
------------

The QLF database keeps information about the QA outputs as well as the pipeline execution.

    .. figure:: _static/qlfdb.png
       :name: qlfdb
       :target: _static/qlfdb.png
       :alt: QLF v0.1 database

       Figure 2. QLF v0.1 database, showing ``Job``, ``Metric`` and associated ``Measurement`` tables.


QA outputs are generically referred as *metrics* here, and are registered in the ``Metric`` table. A metric has ``name``, ``description``, ``condition``
and a ``threshold`` that can be used to trigger alerts.

In QLF v0.1,  this table stores just summary information (e.g. median SNR per ccd). We plan to extend the schema in QLF v0.3 to support
individual and aggregated measurements adding the ``Spectrograph``, ``Ccd`` and ``Fiber`` tables in the schema (e.g. SNR of each fiber
associated to a given CCD and Spetrograph as well as median SNR per CCD or Spectrograph)

Each execution of the pipeline is called a *job* and has ``start``, ``end`` time and a ``status``.

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

.. note::
   In development mode the API can be reached at http://localhost:8000/dashboard/api with user=nobody and password=nobody


Visualization
-------------

In QLF v0.1, we integrated Django and the Bokeh python library, and demonstrate this integration with a dashboard
that lists QA outputs registered in the QLF database (e.g Median SNR) and present an interactive time series plot
showing the values measured by each execution of the QL pipeline (in QLF v0.1 this is a constant value)

A screenshot of the dashboard interface is shown below:

    .. figure:: _static/dashboard.png
       :name: dashboard
       :target: _static/dashboard.png
       :alt: QLF v0.1 dashboard

       Figure 2. QLF v0.1 dashboard, listing QA Outputs and a time series plot.


References
==========

*TODO*

* :ref:`search`

