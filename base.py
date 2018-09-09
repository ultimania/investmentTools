# coding: UTF-8
import io,sys
sys.stdout = io.TextIOWrapper(sys.stdout.buffer,encoding='utf-8')

import urllib.request, urllib.error
from bs4 import BeautifulSoup

# Access URL
url = "http://www.nikkei.com"
html = urllib.request.urlopen(url)
soup = BeautifulSoup(html, "html.parser")

# get title
title_tag = soup.title
title = title_tag.string

# print
print(title_tag)
print(title)


