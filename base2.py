# coding: UTF-8
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import urllib.request, urllib.error
from bs4 import BeautifulSoup
import MySQLdb
from datetime import datetime as dt

# Access URL
url = "https://www.nikkei.com/nkd/company/?scode=8358"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")

db_host = "172.30.20.2"
db_port = "3306"
db_user = "root"
db_pass = "admin"
db_table = "surugagin"
db_name = "db_investment"


#DB Connection
dbconnection = MySQLdb.connect(
    host=db_host,
    user=db_user,
    passwd=db_pass,
    db=db_name,
    charset='utf8'
)
cursor = dbconnection.cursor()

# loop for div
div = soup.find_all("dd")
for tag in div:
    try:
        # get class string
        class_str = tag.get("class").pop(0)
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
    except:
        pass

dbconnection.commit()
dbconnection.close()