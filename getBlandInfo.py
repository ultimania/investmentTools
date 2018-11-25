# coding: UTF-8
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime as dt
import io,sys
import urllib.request, urllib.error
import MySQLdb

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')


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
db_host = "192.168.0.21"
db_port = 3306
db_user = "djangoAdmin"
db_pass = "admin"
db_database = "django"
db_insert_table = "investment_t_stk_prc_tr"

# Scripts
path_select_bland_ms = '/git/ultimania/investmentTools/sql/getBlandInfo_selectBlandMs.sql'

# parameter
datetimestr = dt.now().strftime('%Y%m%d%H%M%S')

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

'''
We will acquire the stock information from T_BLAND_MS.
Only the one whose acquisition flag is valid 
is taken as the stock information to be acquired.

For each stock acquired, 
we perform scraping and get the latest necessary information.
'''
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


    '''
    Get target parameter information from T_TRG_PRM_MS for new cursor.
    We perform scraping based on retrieval tag 
    and class string acquired for each parameter.
    '''

    # Exec SQL Script
    cur2 = conn.cursor()
    sql_string = "SELECT * FROM investment_t_trg_prm_ms"
    cur2.execute(sql_string)
    
    # Dictionary Object
    params = {}

    '''
    Analyze scraping data based on acquired target parameter information.
    '''
    for row_param in cur2:
    
        # T_TRG_PRM_MS.TRG_PRM_NAME
        param_name = row_param[0]
        # T_TRG_PRM_MS.FIND_TAG
        trg_tag = row_param[2]
        # T_TRG_PRM_MS.CLASS_STRING
        class_string = row_param[3]
        # T_TRG_PRM_MS.EXCLUDE_TAGS
        exclude_tags = row_param[4].split(" ")

        # find target tag
        tag = soup.find(trg_tag,class_=class_string)
        
        if tag is not None:
            # exclude tags
            for exclude_tag in exclude_tags:
                if tag.find(exclude_tag) is not None:
                    tag.span.extract() # remove span tag
            if tag.string is not None:
                # delete comma
                params[param_name] = tag.string.replace(",", "")
                # pop class string for next search
                tag.get("class").pop(0)
    

    '''
    After extracting the target values ​​for the number of rows (the number of target parameters),
    insert them into the transaction table of T_STK_PRC_TR.
    '''
    try:
        cur.execute(
            "insert into " + db_insert_table +
            " (market_prod_cls ,current_price ,day_before_ratio ,opening_price ,high_orice ,low_price ,sales_volume ,created_at ,bland_cd_id ) " + 
            "values (%(MARKET_PROD_CLS)s, %(CURRENT_PRICE)s,%(DAY_BEFORE_RATIO)s,%(OPENING_PRICE)s,%(HIGH_PRICE)s,%(LOW_PRICE)s,%(SALES_VOLUME)s,%(CREATE_TIMESTAMP)s,%(BLAND_CD)s)",
            {
                'MARKET_PROD_CLS'   : row[1],           # T_BLAND_MS.MARKET_PROD_CLS
                'CURRENT_PRICE'     : params[1], 
                'DAY_BEFORE_RATIO'  : params[2], 
                'OPENING_PRICE'     : params[3],
                'HIGH_PRICE'        : params[4], 
                'LOW_PRICE'         : params[5],
                'SALES_VOLUME'      : params[6], 
                'CREATE_TIMESTAMP'  : datetimestr,
                'BLAND_CD'          : row[0]           # T_BLAND_MS.BLAND_CD
            }
        )
        conn.commit()

    except:
        pass

conn.close()
