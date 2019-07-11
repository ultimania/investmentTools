# coding: UTF-8
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import codecs, sys, io

class MyScraper():
    def __init__(self):
        pass

    def scrapeWebPage(self, url):
        soup =  BeautifulSoup(
            urllib.request.urlopen(url),
            "html.parser"
        )
        return soup
