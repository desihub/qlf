### Running locally with docker

    # Config file

    ```
    cp framework/config/qlf.cfg.template framework/config/qlf.cfg
    ```

    # Test data for local run of QLF: night 20190101, exposures 3 and 4.

    ```
    mkdir spectro && cd spectro

    wget -c http://portal.nersc.gov/project/desi/data/quicklook/20190101_small.tar.gz 

    # IF using OSX and wget not available, download with curl -O

    # Unzip

    tar xvzf 20190101_small.tar.gz

    rm 20190101_small.tar.gz
    ```

### Running QLF

    ```
    docker-compose up
    ```