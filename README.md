## DESI Quick Look Framework

### Installing DESI QLF locally

1. Install the Quick Look Framework 

    ```
    # We assume you are using bash
    export QLF_ROOT=$HOME/quicklook
    mkdir -p $QLF_ROOT
    cd $QLF_ROOT
   
    git clone https://github.com/desihub/qlf.git
    ```

2. Install software dependencies

    ```
    source ~/miniconda3/bin/activate root
    ```
    
    NOTE: if you don't have conda installed we recommend installing miniconda3 follow the instructions at `https://conda.io/docs/install/quick.html` and make sure ~/miniconda3/bin is in your PATH
   
    ```
    conda config --add channels conda-forge
    conda create --name quicklook python=3.5 --yes --file qlf/requirements.txt
    source activate quicklook
    # Packages not available through conda
    pip install -r qlf/extras.txt
    ```

3. Install the DESI Quick Look pipeline 

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

4. Get test data

    ```
    export DESI_SPECTRO_DATA=$QLF_ROOT/data
    mkdir -p $DESI_SPECTRO_DATA
    cd $DESI_SPECTRO_DATA
    
    # Test data for local run of QLF: night 20170428, exposures 3,4 and all cameras
    wget -c http://portal.nersc.gov/project/desi/data/quicklook/20170428_small.tar.gz
    tar xvzf 20170428.tar.gz
    ```
    
    NOTE: on `desidev@lbl.gov`, you might copy ~1 night of data from `/home/angelofausti/data/20170428.tgz`

### Running QLF 

1. Configure QLF 

    Activate the `quicklook` environment
    
    ```
    source ~/miniconda3/bin/activate quicklook
    export QLF_ROOT=$HOME/quicklook
    ```
    
    Create your `qlf.cfg` file

    ```
    cd $QLF_ROOT/qlf/config
    cp qlf.cfg.template qlf.cfg
    
    ```
    
    Edit `qlf.cfg` (follow the instructions there)
    
    NOTE: in development mode, QLF will process the data specified in the `qlf.cfg`. 
    Each time you run QLF a fresh database is created and the Quick Look outputs are ingested at the end of the processing of each exposure. 

2. Start QLF  

    ```
    cd $QLF_ROOT/qlf/qlf
    ./run.sh
    ```
    
    NOTE: you can follow the progress of the data processing watching `qlf.log` or from the web application.

### Support


    Contact: helpdesk@linea.gov.br
    

