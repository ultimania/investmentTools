# coding: UTF-8
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import codecs, sys, io, os
import django

sys.path.append('/opt/myproject')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myproject.settings') 
django.setup()

from mytrade.models import T_TRG_PRM_MS
from mytrade.models import T_SCALE_MS
from mytrade.models import T_INDUSTRY_MS
from mytrade.models import T_BLAND_MS
from mytrade.models import T_STK_PRC_TR
from mytrade.models import T_EXT_CND_TR
from mytrade.models import T_EXT_CND_CH_TR
from mytrade.models import T_STATISTIC_MS
from mytrade.models import T_UNIT_MS
from mytrade.models import T_CONDITIONS_MS
from mytrade.models import T_URL_MS

class MyTradeDo():

    def getUrls(self, bland_cd='none'):
        self.key = 'access_url_string'

        if(bland_cd == 'none'):
            self.result = T_BLAND_MS.objects.all().values_list(self.key, flat=True)
        else:
            self.result = T_BLAND_MS.objects.filter(bland_cd=bland_cd).values_list(self.key, flat=True)
        return self.result

    def add(self, bland_cd, model_name, contents):
        self.key='market_prod_cls'
        self.bland_data = T_BLAND_MS.objects.filter(bland_cd=bland_cd).values_list(self.key, flat=True)

        if(model_name=='T_STK_PRC_TR'):
            record = T_STK_PRC_TR(
                        bland_cd_id             = int(bland_cd), 
                        market_prod_cls         = self.bland_data,
                        current_price       	= contents[0],
                        day_before_ratio    	= contents[1],
                        opening_price       	= contents[2],
                        high_orice          	= contents[3],
                        low_price           	= contents[4],
                        sales_volume        	= contents[5],
                        exp_per                	= contents[6],
                        exp_dividend_yield     	= contents[7],
                        pbr                    	= contents[8],
                        exp_roe                	= contents[9],
                        exp_stock_gain         	= contents[10],
						common_stock_number    	= contents[11],
						market_capitalization  	= contents[12],
						special_treatment      	= contents[13],
						year_to_date_high_price	= contents[14],
						year_to_date_low_price 	= contents[15],
						years_10_high          	= contents[16],
						years_10_low           	= contents[17],
						trading_unit           	= contents[18],
						minimum_purchase_price 	= contents[19]
            )
            record.save()

    def __init__(self):
        pass

