# coding: UTF-8
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import urllib.request, urllib.error
from bs4 import BeautifulSoup
import MySQLdb
from pprint import pprint


'''
Environment variables and script variables used in scripts 
are defined below.

'database' is an environment variable 
for mysql database connection. 
When the connection destination changes, 
please modify this variable according to the change contents.

'Scripts' is information on the full path of the file
 read from this script.
If input files are added, 
please add file path information to this section.
'''

# Database
db_host = "172.30.20.1"
db_port = 30002
db_user = "kabuAdmin"
db_pass = "admin"
db_database = "db_investment"

# Scripts
path_select_bland_ms = '/git/ultimania/investmentTools/sql/getBlandInfo_selectBlandMs.sql'

'''
Main Process
'''
# Create Database Connection Object
conn = MySQLdb.connect(
    host = db_host,
    port = db_port,
    user = db_user,
    password = db_pass,
    database = db_database,
    charset='utf8'
)
cur = conn.cursor()

# Read SQL Script
file = open(path_select_bland_ms)
sql_string = file.read()
file.close()

import pdb;pdb.set_trace()

# Exec SQL Script
cur.execute(sql_string)
for row in cur:
    pprint(row)
