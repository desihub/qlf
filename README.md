# QLF

Developement of the Quick Look Framework for DESI

## Content

**QLF Daemon** coordinates the execution of QLF pipeline when new data arrives, it creates the QL configuration file launchs N instances of the pipeline, poll QL logs and ingest results in the DB for further visualization

Install procedure:

This tutorial applies to Red Hat 7-based Linux distributions (CentOS 7, etc.). To run on Debian based distributions, the procedure is practically similar, but using apt-get instead of yum.

First, install the following packages (some of them may be already installed):

$ sudo yum install gcc postgresql-server git epel-release postgresql-devel python-devel

Now that we have epel, we're able to install and update python-pip:

$ sudo yum install python-pip && sudo pip install --upgrade pip

We then need these packages to be able to run the code: 

$ sudo pip install python-daemon pyyaml django psycopg2

Now we need to initialize the postgresql database:

$ sudo postgresql-setup initdb

Now we're going to configure postgresql. Open pg_hba.conf with yout favorite editor (as root). Here we use gedit:

$ sudo gedit /var/lib/pgsql/data/pg_hba.conf 

append the following line:

host    all             develdba        127.0.0.1/32            md5

BEFORE THE LINE:

host    all             all             127.0.0.1/32            ident

Make postgresql enabled on the OS startup by running this command:

$ sudo chkconfig postgresql on

Then start the postgresql service:

$ sudo systemctl enable postgresql.service

$ sudo systemctl start postgresql.service

Create the user develdba with password dbadevel (after pressing enter, the console prompts to type the password):

$ sudo -u postgres createuser -d -R -P develdba

Now we create the code database:

$ sudo -u postgres createdb -O develdba qa

The permissions of the user develdba to access the qa database must be set with the following commands:

$ sudo -u postgres psql

Then run the query on the psql console (the second line is needed to exit from the psql console):

postgres=# GRANT ALL PRIVILEGES ON DATABASE qa TO develdba;

postgres=# \q

Go to the folder where the project will be cloned (here we assume the user's home directory, i.e.: ~/). Then clone the repository:

$ cd ~/ && git clone https://github.com/linea-it/qlf

Finally, if everything worked out correctly, we can create the tables on the database by using the following command:

$ python ~/qlf/qlf/manage.py migrate


