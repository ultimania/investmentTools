# coding: UTF-8
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import codecs, sys, io, os
import django

class MyPerser():
    def parse(self, model_name, soup):
        values = []
        
        # 株価情報の取得
        if(model_name=='T_STK_PRC_TR'):
            # 現在値
            html_strings = soup.find(class_="m-stockPriceElm_value now")
            # 現在値が見つからない場合は例外処理
            if(html_strings is None):
                raise ValueError("No m-stockPriceElm_value_now Tag")
            value = html_strings.contents[0]
            values.append(value)
            # 前日比
            if(html_strings is None):
                raise ValueError("No stc-percent Tag")
            html_strings = soup.find(class_="stc-percent")
            value = html_strings.contents[0]
            values.append(value)
            # その他
            for html_strings in soup.find_all(class_="m-stockInfo_detail_value"):
                if(html_strings is None):
                    raise ValueError("No m-stockInfo_detail_value Tag")
                value = html_strings.contents[0]
                values.append(value)
        return values

    def __init__(self):
        pass

