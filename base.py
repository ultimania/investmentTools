# coding: UTF-8
import urllib2
from bs4 import BeautifulSoup

# Access URL
url = "http://www.nikkei.com"
html = urllib2.urlopen(url)
soup = BeautifulSoup(html, "html.parser")

# get title
title_tag = soup.title
title = title_tag.string

# print
print title_tag
print title

