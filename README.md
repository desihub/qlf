# QLF

Developement of the Quick Look Framework for DESI

## Content

**QLF Daemon** coordinates the execution of QLF pipeline when new data arrives, it creates the QL configuration file launchs N instances of the pipeline, poll QL logs and ingest results in the DB for further visualization

Install procedure:

This tutorial applies to Red Hat 7-based Linux distributions (CentOS 7, etc.). To run on Debian based distributions, the procedure is practically similar, but using apt-get instead of yum.

First, install the mirror definitions to postgresql94:

$ sudo yum localinstall http://yum.postgresql.org/9.4/redhat/rhel-6-x86_64/pgdg-centos94-9.4-1.noarch.rpm

Install postgresql94-server, git (to clone the repository), and epel-release (to install python-pip):

$ sudo yum install postgresql94-server git epel-release

Now that we have epel, we're able to install python-pip:

$ sudo yum install python-pip

It's a good practice to upgrade pip:

$ sudo pip install –-upgrade pip

We then need these packages to be able to run the code: 

$ sudo pip install python-daemon

$ sudo pip install pyyaml

$ sudo pip install django

Using pip to install psycopg2 seems to return an error, so we use yum to install it instead:

$ sudo yum install python-psycopg2

Now we are able to initialize the postgres database:

$ sudo /usr/pgsql-9.4/bin/postgresql94-setup initdb

Make postgres enabled by default on the OS by running this command:

$ sudo chkconfig postgresql-9.4 on

Then start the postgres service:

$ sudo systemctl enable postgresql-9.4.service

$ sudo systemctl start postgresql-9.4.service

Create the user develdba with password dbadevel (after pressing enter, the console prompts to type the password):

$ sudo -u postgres createuser -d -R -P develdba

Now we create the code database:

$ sudo -u postgres createdb -O develdba qa

The permissions of the user develdba to access the qa database must be set with the following commands:

$ sudo -u postgres psql

Then run the query on the psql console:

postgres=# GRANT ALL PRIVILEGES ON DATABASE qa TO develdba;

Open pg_hba.conf with yout favorite editor (as root). Here we use vim:

$ sudo vim /var/lib/pgsql/9.4/data/pg_hba.conf 

append the following line

host    all             develdba        127.0.0.1/32            md5

BEFORE THE LINE:

host    all             all             127.0.0.1/32            ident

Then restart the service:

$ sudo systemctl restart postgresql-9.4.service

Go to the folder where the project will be cloned (here we assume the user's home directory, i.e.: ~/):

$ cd ~/

Then clone the repository:

$ git clone https://github.com/linea-it/qlf

Then go to the django root folder 'qlf'. it is located inside the folder where the qlf project is cloned (we assume ~/qlf/qlf):

$ cd ~/qlf/qlf

Finally, we create the tables using the following command:

$ python manage.py migrate
