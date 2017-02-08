# QLF

Development of the Quick Look Framework (QLF) for DESI

http://quick-look-framework.readthedocs.io

## Cloning the project

```
  $ git clone https://github.com/linea-it/qlf.git
```

## Create a virtualenv and install software dependencies
```
  $ cd qlf
  $ virtualenv env -p python3
  $ source env/bin/activate
  $ pip install -r requirements.txt
```

## Run QLF in development mode
```
  $ cd qlf
  $ ./run.sh
```
the first time you will be asked to set a database password for your user.

The dashboard API will run on http://localhost:8000/dashboard/api

Open another terminal and start the Bokeh server:

```
  $ cd qlf
  $ source env/bin/activate
  $ cd viz
  $ ./bokeh.sh
```
The bokeh apps will run on http://localhost:5006


## Compile the QLF documentation
```
  $ cd qlf
  $ source env/bin/activate
  $ cd docs
  $ make html
```

open the documentation at ```qlf/docs/_build/html/index.html```
