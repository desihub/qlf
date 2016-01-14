# QLF

Developement of the Quick Look Framework for DESI

## Content

**QLF Daemon** coordinates the execution of QLF pipeline when new data arrives, it creates the QL configuration file launchs N instances of the pipeline, poll QL logs and ingest results in the DB for further visualization

Dependencies:

python-daemon
pyyaml

To install the dependencies, it's highly reccomended to use pip:

$ sudo apt-get install python-pip (Debian-based distributions)
or
$ sudo yum install python-pip (Red-Hat based distributions)

then:

$ sudo pip install python-daemon
$ sudo pip install pyyaml



