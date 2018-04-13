## DESI Quick Look Framework User Interface

The Quick Look Framework is part of the DES Instrument Control System (ICS) and provides an interface to execute the Quick Look (QL) pipeline and display data quality information in realtime. 

The interfaces for QA display are now in a mature stage of development using React and Bokeh plots.

This project requires [QLF](https://github.com/desihub/qlf) to show available data.

### Clone Quick Look Framework Project

    git clone https://github.com/desihub/qlf-ui.git
    cd qlf-ui
    cp .env.template .env

## Running locally with docker

- `docker-compose up`

## Accessing the interface

- http://localhost:3000/


_To connect with the `qlf api` you must follow [qlf docker installation](https://github.com/desihub/qlf/blob/master/DOCKER.md)_

## Stopping and reseting QLF-UI

- `docker-compose stop`

## Deployment

- [Example deploy using docker and nginx.](https://github.com/desihub/qlf-ui/blob/master/DEPLOY.md)

### Support


    Contact: helpdesk@linea.gov.br
