# coding: UTF-8
from bs4 import BeautifulSoup
from pprint import pprint
from datetime import datetime as dt
import io,sys
import codecs
import urllib.request, urllib.error
import MySQLdb

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

class myScraper:

    '''--------------------------------------------------------------------------
    functions
    --------------------------------------------------------------------------'''
    def __init__(self):
        super().__init__()

    def model
        urls = T_BLAND_MS.objects.all().order_by(access_url_string)
        target_url = re.sub(r'page=[0-9]+', 'page=' + str(page_count), base_url) 
        soup =  BeautifulSoup(
                    urllib.request.urlopen(target_url),
                    "html.parser"
                )



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

