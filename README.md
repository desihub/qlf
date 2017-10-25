## DESI Quick Look Framework

The Quick Look Framework is part of the DES Instrument Control System (ICS) and provide interfaces for executing the quick look pipeline and display data quality information in realtime. 

In the current version it is possible to control the execution of the quicklook pipeline through the interface, process multiple cameras in paralel and follow the progress of the data reduction. The interfaces for QA display are still in initial stage of development. Your suggestions and comments to improve this system are very welcome!  

See a presentation from June 2017 [here](https://desi.lbl.gov/DocDB/cgi-bin/private/ShowDocument?docid=3024).

### Installing DESI QLF locally

1. Install the Quick Look Framework 

    ```
    # We assume you are using bash. It is useful to add this to your .bashrc file (or related)
    export QLF_ROOT=$HOME/quicklook
    mkdir -p $QLF_ROOT
    cd $QLF_ROOT
   
    git clone https://github.com/desihub/qlf.git
    cd qlf
    git checkout merge_qa_ohio
    cd ..
    ```

2. Install software dependencies and create miniconda environment 

    NOTE: install miniconda3 following instructions [here](https://conda.io/docs/install/quick.html) and make sure ~/miniconda3/bin is in your PATH by running `echo $PATH` and checking your .bashrc (or related)

    ```
    source ~/miniconda3/bin/activate root
    ```
   
    ```
    conda config --add channels conda-forge
    conda create --name quicklook python=3.5 --yes --file qlf/requirements.txt
    source activate quicklook 
    pip install -r qlf/extras.txt
    ```

3. Install the DESI Quick Look pipeline 

    ```
    cd $QLF_ROOT
    git clone https://github.com/desihub/desispec.git 
    git clone https://github.com/desihub/desiutil.git
    cd desispec
    git checkout 885661aa99b29f151c95b3a16d08e43a8e572080
    cd ../desiutil
    git checkout 1.9.7
    cd ..
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
    
4. Get test data (~1 GB)

    ```
    mkdir -p $QLF_ROOT/spectro # or any other place, make sure this path is consistent with qlf.cfg in step 5.
    cd $QLF_ROOT/spectro
    
    # Test data for local run of QLF: night 20190101, exposures 3 and 4.
 
    wget -c http://portal.nersc.gov/project/desi/data/quicklook/20190101_small.tar.gz 
    
    # IF using OSX and wget not available, download with curl -O
    
    tar xvzf 20190101_small.tar.gz
    
    # This creates two directories: data and redux which should be exported as environment variables that goes on qlf.cfg in step 5

    export DESI_SPECTRO_DATA=$QLF_ROOT/spectro/data
    export DESI_SPECTRO_REDUX=$QLF_ROOT/spectro/redux

    ```

5. Configure QLF

   
    Create your `qlf.cfg` file

    ```
    cd $QLF_ROOT/qlf/config
    cp qlf.cfg.template qlf.cfg
    
    ```
    
    Edit `qlf.cfg` (follow the instructions there)
    
    NOTE: in development mode, QLF will process the data in the path specified in the `qlf.cfg`. 
    Each time you run QLF a fresh database is created and the Quick Look outputs are ingested after each exposure is processed. 



### Running QLF

1. Activate the `quicklook` environment and export paths
    
    ```
    source ~/miniconda3/bin/activate quicklook
    export QLF_ROOT=$HOME/quicklook
    export DESI_SPECTRO_DATA=$QLF_ROOT/spectro/data
    export DESI_SPECTRO_REDUX=$QLF_ROOT/spectro/redux
    export QL_SPEC_DATA=$DESI_SPECTRO_DATA
    export QL_SPEC_REDUX=$DESI_SPECTRO_REDUX


    ```

2. Start QLF
    ```
    cd $QLF_ROOT/qlf/qlf
    ./run.sh
    ```
    
    NOTE: you can follow the progress of the data processing watching `$QLF_ROOT/qlf.log` or from the web application at http://localhost:8000.

### Support


    Contact: helpdesk@linea.gov.br
    

