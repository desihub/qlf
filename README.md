# QLF

Developement of the Quick Look Framework for DESI

## Content

**QLF Daemon** coordinates the execution of QLF pipeline when new data arrives, it creates the QL configuration file launchs N instances of the pipeline, poll QL logs and ingest results in the DB for further visualization

Dependencies:

python-daemon
python-yaml

To install the dependencies, the appropriate package manager must be used:

$ sudo apt-get install python-yaml    (Debian based distributions)
$ sudo yum install python-yaml        (Red-Hat based distributions)
