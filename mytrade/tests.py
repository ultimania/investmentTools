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

    # 銘柄情報取得
    try:
        bland_info = mytradedo.getBlandInfo()
    except (ValueError, IndexError) as ex:
        p(ex)

    # スクレイピング実行
    for data in bland_info:
        # import pdb;pdb.set_trace()
        soup = myscraper.scrapeWebPage(data['access_url_string'])
        if(soup is not None):
            try:
                contents = myparser.parse('T_STK_PRC_TR', soup)
                mytradedo.add(data['bland_cd'] ,'T_STK_PRC_TR', contents)
            except ValueError as e:
                print(e)
