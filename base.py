# coding: UTF-8
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import urllib.request, urllib.error
from bs4 import BeautifulSoup
import MySQLdb
from pprint import pprint
from datetime import datetime as dt


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
db_insert_table = "T_STK_PRC_TR"

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
    
    'class_string' is the name of the class attached 
    to the tag surrounding the acquisition target.
    '''
    url = row[9] # T_BLAND_MS.ACCESS_URL_STRING
    html = urllib.request.urlopen(url)
    soup = BeautifulSoup(html, "html.parser")
    tag = "dd"
    class_string = "m-stockPriceElm_value"
    
    tags = soup.find_all(tag)
    for tag in tags:
        # find class string
        if tag.get("class").pop(0) in class_string:
            tag.span.extract() # remove span tag
            if tag.string is not None:
                try:
                    # delete comma
                    current_price = tag.string
                    current_price = current_price.replace(",", "")

                    # TableInsert
                    datetimestr = dt.now().strftime('%Y%m%d%H%M%S')
                    cur.execute(
                        "insert into " + db_insert_table + " values (%(BLAND_CD)s, %(MARKET_PROD_CLS)s, %(CURRENT_PRICE)s,%(DAY_BEFORE_RATIO)s,%(OPENING_PRICE)s,%(LOW_PRICE)s,%(SALES_VOLUME)s,%(CREATE_TIMESTAMP)s)",
                        {
                            'BLAND_CD': row[0], # T_BLAND_MS.BLAND_CD
                            'MARKET_PROD_CLS': row[1], # T_BLAND_MS.MARKET_PROD_CLS
                            'CURRENT_PRICE': int(current_price),
                            'DAY_BEFORE_RATIO': 1, 
                            'OPENING_PRICE': 1,
                            'HIGH_PRICE': 1, 
                            'LOW_PRICE': 1,
                            'SALES_VOLUME': 1, 
                            'CREATE_TIMESTAMP': datetimestr
                        }
                    )
        except:
            pass

conn.commit()
conn.close()