from django.test import TestCase
import sys, io

# scraper Module
from scraper.mytradedo import MyTradeDo
from scraper.myscraper import MyScraper
from scraper.myparser import MyPerser

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Create your tests here.
if __name__ == "__main__":
    # インスタンス生成
    mytradedo = MyTradeDo()
    myscraper = MyScraper()
    myparser = MyPerser()

    soups = []

    bland_cd = '1301'

    # 対象URL取得
    try:
        urls = mytradedo.getUrls(bland_cd)
    except (ValueError, IndexError) as ex:
        p(ex)

    # スクレイピング実行
    for url in urls:
        soup = myscraper.scrapeWebPage(url)
        soups.append(soup)

    # タグ解析
    for soup in soups:
        import pdb;pdb.set_trace()
        contents = myparser.parse('T_STK_PRC_TR', soup)
        mytradedo.add(bland_cd, 'T_STK_PRC_TR', contents)

