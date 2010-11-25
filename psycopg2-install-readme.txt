To install psycopg2 (needed for PostgreSQL connection) in a virtualenv do the following: 

http://blog.serverhorror.com/2010/04/28/python-psycopg2-postgresql84-and-mac-os-x-snow-leopard/

In my system (Mac OS x 10.6) i had to use these commands (different postgres path) and python 2.5 (not 2.6): 

virtualenv -p python2.5 --no-site-packages .
. bin/activate
easy_install  -U setuptools
easy_install pip
PATH=$PATH:/Library/PostgreSQL/8.4/bin pip install psycopg2