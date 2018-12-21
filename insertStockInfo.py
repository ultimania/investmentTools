# coding: UTF-8
import MySQLdb
import os
import json
import datetime
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

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
path_result_folder  = script_base + '/result'
result_files        = [f for f in os.listdir(path_result_folder) if os.files.isfile(os.path.join(path_result_folder, f))]
path_sql_folder     = script_base + '/sql'
sql_insert_stockprice = path_sql_folder + '/insertStockPrice.sql'

# Output files
path_result_json    = script_base + '/result/getValue_' + datetimestr + '.json'

'''--------------------------------------------------------------------------
my functions
--------------------------------------------------------------------------'''
def normalizeRecord(record: 'data array of data set') -> 'normalized data':
    '''--------------------------------------
    date format convert : record[3]
      "mm/dd hhmm" -> " yyyy/mm/dd hh:mm:ss "
    --------------------------------------'''
    t_datetime = datetime.datetime.strptime( record[3], '%m/%d %H%M')
    record[3] = t_datetime.strftime('%Y/%m/%d %H:%M:%S')

    '''--------------------------------------
    delete comma from integer value : record[4],record[7],record[8]
      "n,nnn" -> "nnnn"
    --------------------------------------'''
    record[4] = record[4].string.replace(",", "")
    record[7] = record[7].string.replace(",", "")
    record[8] = record[8].string.replace(",", "")

    return record

def genInsertSql(record: 'normalized data') -> 'sql strings'
    # Read SQL Script
    with open(sql_insert_stockprice) as f:
        sql_string = f.read()
    sql_string.format(
        TABLE_NAME        = db_insert_table,
        MARKET_PROD_CLS   = record[2],
        CURRENT_PRICE     = record[4],
        DAY_BEFORE_RATIO  = record[5],
        OPENING_PRICE     = -1,
        HIGH_PRICE        = -1,
        LOW_PRICE         = -1,
        SALES_VOLUME      = record[7],
        CREATE_TIMESTAMP  = record[3],
        BLAND_CD          = record[0]
    )
    return sql_string



'''--------------------------------------------------------------------------
Main Process
--------------------------------------------------------------------------'''
# Get list of result directory
for result_file in result_files:
    '''--------------------------------------
    Read JSON file and convert to list
    --------------------------------------'''
    # Read and Execute SQL Script
    data_set = json.load(path_result_folder + result_file)
    '''--------------------------------------
    Normalize data and create insert SQL
    --------------------------------------'''
    sql_set = []
    for data in data_set:
        sql_string = genInsertSql( normalizeRecord(data) )
        sql_set.append(sql_string )
    '''--------------------------------------
    Connect Database and execute SQL
    --------------------------------------'''
    # Get target value as list
    with MySQLdb.connect(host = db_host, port = db_port, user = db_user, password = db_pass, database = db_database, charset='utf8') as cur:
        cur.execute(sql_set)
    '''--------------------------------------
    Remove result file
    --------------------------------------'''
    os.remove(path_result_folder + result_file)