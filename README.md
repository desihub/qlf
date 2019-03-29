## DESI Quick Look Framework

The Quick Look Framework (QLF) is part of the DES Instrument Control System (ICS) and provides an interface to execute the Quick Look (QL) pipeline and display data quality information in realtime. 

QLF current version allows to follow the execution of QL pipeline, which process multiple cameras/arms in parallel. The interfaces for QA display are now in a mature stage of development using React and Bokeh plots.

_Requires ~2 GB_

### Install Docker

We use Docker as a container to install QLF. Install `docker` and `docker-compose` from the links below:

- [docker](https://docs.docker.com/install/)
- [docker-compose](https://docs.docker.com/compose/install/)

_Make sure `docker --version`, `docker-compose --version`, and `docker ps` runs without error._

### Clone Quick Look Framework Project

    git clone https://github.com/desihub/qlf.git
    
_Everything you need is contained in this repository. Even `desimodel`, `desisim`, `desitarget`, `desispec` and `desiutil` as sub-repositories._

### Install default qlf configuration

Get into `qlf` directory and configure it. 

_Make sure you have [svn](https://subversion.apache.org/packages.html) installed_

    cd qlf
    ./configure.sh

_Besides setting the environment and cloning desispec and desiutil, this downloads the [data](http://portal.nersc.gov/project/desi/data/quicklook/20190101_small.tar.gz) used for tests (~1 GB)._

### Starting QLF

Start QLF frontend and backend.

    ./start.sh

_frontend takes about 5 minutes to start on dev mode_

### User Interface

You can access QLF interface by going to 

    http://localhost/

### Stoping QLF

    ./stop.sh

### Full Documentation
[![Documentation Status](https://readthedocs.org/projects/qlf/badge/?version=latest)](https://qlf.readthedocs.io/en/latest/?badge=latest)

Please visit [qlf on Read the Docs](https://qlf.readthedocs.io/en/latest/). 


### Support


    Contact: helpdesk@linea.gov.br
