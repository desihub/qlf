## DESI Quick Look Framework

See development documentation at http://quick-look-framework.readthedocs.io

### Install DESI QLF locally

1. Install the Quick Look Framework (first time installation)

    ```
    export QLF_ROOT=$HOME/quicklook
    mkdir -p $QLF_ROOT
    cd $QLF_ROOT
   
    git clone https://github.com/linea-it/qlf.git
    ```

2. Install software dependencies (first time installation)

    ```
    source ~/miniconda3/bin/activate
    ```
    
    NOTE: miniconda3 can be installed from https://conda.io/docs/install/quick.html
   
    ```
    conda config --add channels conda-forge
    conda create --name quicklook python=3.5 --yes --file qlf/requirements.txt
    source activate quicklook
    # Packages not available through conda
    pip install -r qlf/extras.txt
    ```

3. Install the DESI Quick Look pipeline (first time installation)

    ```
    cd $QLF_ROOT
    git clone https://github.com/desihub/desispec.git
    git clone https://github.com/desihub/desiutil.git
    ```
  
    Test if DESI Quick Look pipeline is available (optional)
    ```
    for package in desispec desiutil; do
        echo "Setting $package..."
        export PATH=$QLF_ROOT/$package/bin:$PATH
        export PYTHONPATH=$QLF_ROOT/$package/py:$PYTHONPATH
    done
    
    desi_quicklook --help
    ```

4. Get test data (first time installation)

    ```
    export DESI_SPECTRO_DATA=$HOME/data
    mkdir -p $DESI_SPECTRO_DATA
    cd $DESI_SPECTRO_DATA
    
    # Test data for local run of Quick Look, night 20170428, exposures 3,4 and all cameras
    wget -c http://portal.nersc.gov/project/desi/data/quicklook/20170428_small.tar.gz
    ```
    
    NOTE: on desidev server, you migth copy ~1 night of data from `/home/angelofausti/data/20170428.tgz`

5. Configure QLF 

    ```
    cd $QLF_ROOT/qlf/config
    
    # Configuration template
    cp qlf.cfg.template qlf.cfg
    
    Update the qlf.cfg file with local paths for the input data, log files, etc.
    ```
    
    NOTE: in development mode, QLF will process the data specified in the `qlf.cfg`. Each time you run QLF a fresh database is created and the results are ingested at the end of the processing of each exposure. 

6. Start QLF  

    ```
    source ~/miniconda3/bin/activate
    source activate quicklook
    export QLF_ROOT=$HOME/quicklook
    cd $QLF_ROOT/qlf/qlf
    ./run.sh
    ```
    
    NOTE: you can follow the progress of data processing from `qlf.log` or from the web application.
    

