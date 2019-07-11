# coding: UTF-8
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import codecs, sys, io, os
import django

class MyPerser():
    def parse(self, model_name, soup):
        values = []
        if(model_name=='T_STK_PRC_TR'):
            # 現在値
            html_strings = soup.find(class_="m-stockPriceElm_value now")
            value = html_strings.contents[0]
            values.append(value)
            # 前日比
            html_strings = soup.find(class_="m-stockPriceElm_value comparison plus")
            values.append(html_strings.contents[0])
            # その他
            for html_strings in soup.find_all(class_="m-stockInfo_detail_value"):
                value = html_strings.contents[0]
                values.append(value)
        return values

    def __init__(self):
        pass

