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

    def getBlandInfo(self, bland_cd=''):
        if(bland_cd==''):
            filters={}
        else:
            filters={"bland_cd": bland_cd}

        self.result = T_BLAND_MS.objects.filter(**filters).values(
            'bland_cd',
            'bland_name',
            'market_prod_cls',
            'industry_cd',
            'sub_industry_cd',
            'scale_cd',
            'fetch_flg',
            'access_url_string',
        )
        return self.result

    def normalizationValue(self, value):
        if(value=='N/A'):
            result = '0'
        else:
            result = value.translate(str.maketrans({
                '(' : '',
                ')' : '',
                ',' : '',
                '-' : '0'
            }))
        return result

    def add(self, bland_cd, model_name, contents):
        # 株価情報
        if(model_name=='T_STK_PRC_TR'):
            self.bland_data = self.getBlandInfo(bland_cd)
            record = T_STK_PRC_TR(
                bland_cd_id             = int(bland_cd), 
                market_prod_cls         = self.bland_data[0]['market_prod_cls'],
                current_price       	= float(self.normalizationValue(contents[0])),
                day_before_ratio    	= contents[1].translate(str.maketrans({'(':'', ')':''})),
                opening_price       	= float(self.normalizationValue(contents[2])),
                high_orice          	= float(self.normalizationValue(contents[3])),
                low_price           	= float(self.normalizationValue(contents[4])),
                sales_volume        	= int(self.normalizationValue(contents[5])),
                exp_per                	= float(self.normalizationValue(contents[6])),
                exp_dividend_yield     	= float(self.normalizationValue(contents[7])),
                pbr                    	= float(self.normalizationValue(contents[8])),
                exp_roe                	= float(self.normalizationValue(contents[9])),
                exp_stock_gain         	= float(self.normalizationValue(contents[10])),
                common_stock_number    	= float(self.normalizationValue(contents[11])),
                market_capitalization  	= float(self.normalizationValue(contents[12])),
                special_treatment      	= contents[13],
                year_to_date_high_price	= float(self.normalizationValue(contents[14])),
                year_to_date_low_price 	= float(self.normalizationValue(contents[15])),
                years_10_high          	= float(self.normalizationValue(contents[16])),
                years_10_low           	= float(self.normalizationValue(contents[17])),
                trading_unit           	= float(self.normalizationValue(contents[18])),
                minimum_purchase_price 	= float(self.normalizationValue(contents[19]))
            )
            record.save()

    def __init__(self):
        pass

