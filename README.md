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

## Run QLF demo in development mode
```
  $ cd qlf
  $ ./run.sh
```

the first time you will be asked to set a database password for your user.

Open another terminal and start the Bokeh server:

```
  $ cd ..
  $ source env/bin/activate
  $ cd qlf
  $ ./bokeh.sh
```

The dashboard will run on http://localhost:8000


## Compile the QLF documentation
```
  $ cd qlf
  $ source env/bin/activate
  $ cd docs
  $ make html
```

open the documentation at ```qlf/docs/_build/html/index.html```
