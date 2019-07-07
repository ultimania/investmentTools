'''--------------------------------------------------------------------------
Main Process
--------------------------------------------------------------------------'''
# Create Database Connection Object
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
