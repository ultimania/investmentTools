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

    '''
    Set parameters necessary for scraping process.
    
    'url' is a URL string for accessing the scrape destination page. 
    Because it is a different URL for each issue, 
    it is acquired from the record set.
    
    'html' is the HTML object obtained by the urllib.request module.
    
    'soup' is an object that uses BeautifulSoup 
    to format the contents of the HTML object.
    
    'tag' is an html tag enclosing the value to be retrieved.
    
    'class' is the name of the class attached 
    to the tag surrounding the acquisition target.
    '''
    url = row[9] # T_BLAND_MS.ACCESS_URL_STRING
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    tag = "dd"
    class = "m-stockPriceElm_value"
    
    div = soup.find_all("dd")
    for tag in div:
        try:
            # find class for "m-stockPriceElm_value now"
            if class_str in 'm-stockPriceElm_value':
                tag.span.extract() # remove span tag
                print(tag.string)
        
                # TableInsert
                datetimestr = dt.now().strftime('%Y%m%d')
                cursor.execute(
                    "insert into " + db_table + " values (%(id)s, %(value)s, %(date)s)",
                    {
                        'id': 1,
                        'value': tag.string, 
                        'date': datetimestr
                    }
                )
        
                break
    
    
