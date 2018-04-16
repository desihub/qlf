## DESI Quick Look Framework

The Quick Look Framework (QLF) is part of the DES Instrument Control System (ICS) and provides an interface to execute the Quick Look (QL) pipeline and display data quality information in realtime. 

QLF current version allows to follow the execution of QL pipeline, which process multiple cameras/arms in parallel. The interfaces for QA display are now in a mature stage of development using React and Bokeh plots.

The project is organized into two repositories, [qlf](https://github.com/desihub/qlf) itself, for the back-end, and Quick Look Framework User Interface ([qlf-ui](https://github.com/desihub/qlf-ui)), for the front-end.
We start with qlf install instructions and provide a link to [qlf-ui instructions](https://github.com/desihub/qlf-ui)

## Installing qlf on your computer

1. Start by cloning qlf project

    git clone https://github.com/desihub/qlf.git
    cd qlf
    git submodule init
    git submodule update

1. QLF User Interface

- Install qlf-ui (front-end) following instructions on https://github.com/desihub/qlf-ui

1. Installing and running qlf

- [Docker installation](https://github.com/desihub/qlf/blob/master/DOCKER.md) (__official__)

## Site deployment

This is not part of the local installation. 
Only follow this if you need to deploy QLF to a site like http://ql.linea.gov.br

- [Example deploy using docker and nginx.](https://github.com/desihub/qlf/blob/master/DEPLOY.md)

### Support

    Contact: helpdesk@linea.gov.br
