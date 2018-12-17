# coding: UTF-8
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime as dt
import io,sys
import urllib.request, urllib.error
import MySQLdb

sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

'''
Environment variables and script variables used in scripts are defined below.
'''
# Database
db_host             = "192.168.0.22"
db_port             = 3306
db_user             = "djangoAdmin"
db_pass             = "admin"
db_database         = "django"
db_insert_table     = "investment_t_stk_prc_tr"
                    
# Scripts          
script_base         = '/root/myproject/investmentTools'
path_getUtl         = script_base + '/sql/getUrl.sql'
path_getTrgPrm      = script_base + '/sql/getTrgPrm.sql'
                    
# Dictionary        
params              = {}
                    
# parameter      
datetimestr         = dt.now().strftime('%Y%m%d%H%M%S')

# Output files
path_result_json    = script_base + '/result/getValue_' + datetimestr + '.json'

'''
my functions
'''
def getIterSoup(base_url: 'base url for scraping',tag_info: 'tag informations as record set', page_size: 'page size for web site') -> 'iteration object for scrapeing result':
    page_count = 0
    while True:
        '''
        Initialized variable
        '''
        result_object = list()  
        tags_object = list()      

        '''
        Exit function when counter reaches page size
        '''
        if page_count > page_size:
            break

        '''
        Scrape the page and create result obuject
        '''
        # decide URL strings and create SOUP object(scrape web page)
        import re
        target_url = re.sub(r'page=[0-9]+', 'page=' + str(page_count), base_url) 
        soup =  BeautifulSoup(
                    urllib.request.urlopen(target_url),
                    "html.parser"
                )

        # Extract Values from html tags
        for row_param in tag_info:
            # Define tags info
            param_id        = row_param[0]
            find_tag        = row_param[2]
            find_class      = row_param[3]
            exclude_tags    = row_param[4]
    
            # Get html strings for find tag
            values = soup.find_all(find_tag, class_=find_class)
            if values is not None and len(values) != 0:
                for value in values:
                    # Add result object
                    tags_object.append( value.string )
            result_object.append({str(page_count) + ':' + find_class + ':' + find_tag : tags_object})
        
        '''
        Return result object
        '''
        yield result_object
        page_count += 1

'''
Main Process
'''
# Create Database Connection Object
with MySQLdb.connect(host = db_host, port = db_port, user = db_user, password = db_pass, database = db_database, charset='utf8') as cur:

    '''
    Get URL information and create soup object for scraping
    '''
    # Read and Execute SQL Script
    with open(path_getUtl) as f:
        cur.execute(f.read())
    # Define scraping info
    for row in cur:
        base_url    = row[1]
        pages       = row[3]

    '''
    Get target parameter information.
    '''
    # Read and Execute SQL Script
    with open(path_getTrgPrm) as f:
        cur.execute(f.read())

    '''
    Get target value and output JSON file
    '''
    import json

    # Get target value as list
    value_list = list()
    for values in getIterSoup(base_url,cur,pages):
        value_list.append(values)

    # output JSON file
    with open(path_result_json, mode='w') as f:
        f.write(json.dumps(value_list))


