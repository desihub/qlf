## DESI Quick Look Framework

See development documentation at http://quick-look-framework.readthedocs.io

### Run DESI QLF locally

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
    
    Note: miniconda3 can be installed from https://conda.io/docs/install/quick.html
   
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
  
    for package in desispec desiutil; do
        echo "Setting $package..."
        export PATH=$QLF_ROOT/$package/bin:$PATH
        export PYTHONPATH=$QLF_ROOT/$package/py:$PYTHONPATH
    done
    ```
    
    At this point the QL pipeline should be available in your terminal
    
    ```
    desi_quicklook --help
    ```

4. Download some test data

    ```
    export DESI_SPECTRO_DATA=$HOME/data
    cd $DESI_SPECTRO_DATA
    wget -c ...

    ```
 

5. Start the web application

    ```
    source activate quicklook 
    cd $QLF_ROOT/qlf/qlf
    ./run.sh
    ```
    
    Open another terminal and start the bokeh server:
    
    ```
    source activate quicklook 
    cd $QLF_ROOT/qlf/qlf
    ./bokeh.sh
    ```
    
Quick Look web application should be available at `http://localhost:8000`


6. Start the Quick Look daemon


    <put command to start Quick Look daemon here>

