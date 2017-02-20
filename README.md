## QLF

### Quick Look Framework (QLF) for DESI

See development documentation at http://quick-look-framework.readthedocs.io

### Run QLF in development mode

1. Clone the project, create a virtualenv and install dependencies

```
  git clone https://github.com/linea-it/qlf.git
  cd qlf
  virtualenv env -p python3
  source env/bin/activate
  pip install -r requirements.txt
```

2. Start the django app
```
  cd qlf
  ./run.sh
```

3. Open another terminal and start the bokeh server:
```
  cd qlf
  source env/bin/activate
  cd qlf
  ./bokeh.sh
```

QLF will run on `http://localhost:8000`

