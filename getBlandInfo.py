# coding: UTF-8
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime as dt
import io,sys
import codecs
import urllib.request, urllib.error
import MySQLdb

'''--------------------------------------------------------------------------
Environment variables and script variables used in scripts are defined below.
--------------------------------------------------------------------------'''
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
                    
# parameter      
datetimestr         = dt.now().strftime('%Y%m%d%H%M%S')

# Output files
path_result_json    = script_base + '/result/getValue_' + datetimestr + '.json'

'''--------------------------------------------------------------------------
my functions
--------------------------------------------------------------------------'''
def recombineList(list1:'sourceList', list2:'targetList') -> 'recombinedList':
    if len(list1) != len(list2) : raise ValueError
    for i in range(0,len(list1)): 
        list1[i].extend(list2[i])
    return list1

def getIterSoup(base_url: 'base url for scraping',tag_info: 'tag informations as record set', page_size: 'page size for web site') -> 'iteration object for scrapeing result':
    import re

    page_count = 0

    '''--------------------------------------
    Scrape the page and create result obuject
    --------------------------------------'''
    while True:
        result_object = list()  
        if page_count > page_size: break

        # decide URL strings and create SOUP object(scrape web page)
        target_url = re.sub(r'page=[0-9]+', 'page=' + str(page_count), base_url) 
        soup =  BeautifulSoup(
                    urllib.request.urlopen(target_url),
                    "html.parser"
                )

        # Extract Values from html tags
        j = 0
        for row_param in tag_info:
            j += 1
            # Define tags info
            param_id        = row_param[0]
            find_tag        = row_param[2]
            find_class      = row_param[3]
            exclude_tags    = row_param[4]
    
            # Get html strings for find tag
            tags_object,tmp_list = list(),list()
            values = soup.select(find_class)
            i, pp  = 0, 3 * j
            if values is not None and len(values) != 0:
                for value in values:
                    tmp_list.insert(i % pp , value.string)
                    if i % pp == pp - 1:
                        tags_object.append(tmp_list)
                        tmp_list = list()
                    i += 1
                result_object.append( tags_object )

        '''--------------------------------------
        Return result object
        --------------------------------------'''
        yield recombineList(result_object[0],result_object[1])
        page_count += 1

'''--------------------------------------------------------------------------
Main Process
--------------------------------------------------------------------------'''
# Create Database Connection Object
with MySQLdb.connect(host = db_host, port = db_port, user = db_user, password = db_pass, database = db_database, charset='utf8') as cur:
    import json

    '''--------------------------------------
    Get URL information and create soup object for scraping
    --------------------------------------'''
    # Read and Execute SQL Script
    with open(path_getUtl) as f:
        cur.execute(f.read())
    # Define scraping info
    for row in cur:
        base_url    = row[1]
        pages       = row[3]

    '''--------------------------------------
    Get target parameter information.
    --------------------------------------'''
    # Read and Execute SQL Script
    with open(path_getTrgPrm) as f:
        cur.execute(f.read())

    '''--------------------------------------
    Get target value and output JSON file
    --------------------------------------'''
    # Get target value as list
    value_list = list()
    for values in getIterSoup(base_url,cur,pages):
        value_list.extend(values)

    with open(path_result_json, mode='w') as f:
        json.dump(value_list, f, ensure_ascii=True, indent=4, sort_keys=True, separators=(',', ': '))



