# QLF

Development of the Quick Look Framework (QLF) for DESI

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
  $ ./bokeh.sh
```

The dashboard will run on http://localhost:8000


## Compile the QLF documentation
```
  $ cd docs
  $ make html
```

