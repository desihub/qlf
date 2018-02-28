## DESI Quick Look Framework

The Quick Look Framework (QLF) is part of the DES Instrument Control System (ICS) and provides an interface to execute the Quick Look (QL) pipeline and display data quality information in realtime. 

QLF current version allows to follow the execution of QL pipeline, which process multiple cameras/arms in parallel. The interfaces for QA display are now in a mature stage of development using React and Bokeh plots.

### Clone Quick Look Framework Project

    git clone https://github.com/desihub/qlf.git
    cd qlf
    git submodule init
    git submodule update

### Running

- [Docker installation](https://github.com/desihub/qlf/blob/master/DOCKER.md) or  [Manual installation](https://github.com/desihub/qlf/blob/master/MANUAL.md)


## Deployment

- [Example deploy using docker and nginx.](https://github.com/desihub/qlf/blob/master/DEPLOY.md)

### QLF User Interface

- To install and use our current Quick Look Framework User Interface follow instructions on https://github.com/desihub/qlf-ui

### Support


    Contact: helpdesk@linea.gov.br
