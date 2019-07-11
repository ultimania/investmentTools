# coding: UTF-8
from bs4 import BeautifulSoup
import urllib.request, urllib.error
import codecs,sys

sys.stdout = codecs.getwriter('utf_8')(sys.stdout)

class MyScraper:
    '''--------------------------------------------------------------------------
    functions
    --------------------------------------------------------------------------'''
    def __init__(self):
        pass

    def scrapeWebPage(self):
        self.mytradedo = MyTradeDo()
        try:
            self.urls = mytradeDo.getUrls(bland_cd)
        except (ValueError, IndexError) as ex:
            p(ex)

        for url in urls:
            self.soup =  BeautifulSoup(
                urllib.request.urlopen(target_url),
                "html.parser"
            )


class MyTradeDo:

    '''--------------------------------------------------------------------------
    Functions
    --------------------------------------------------------------------------'''
    def __init__(self):
        initVariables()

    def initVariables(self):
        t_trg_prm_ms    =  T_TRG_PRM_MS()
        t_scale_ms      =  T_SCALE_MS()
        t_industry_ms   =  T_INDUSTRY_MS()
        t_bland_ms      =  T_BLAND_MS()
        t_stk_prc_tr    =  T_STK_PRC_TR()
        t_statistic_ms  =  T_STATISTIC_MS()
        t_unit_ms       =  T_UNIT_MS()
        t_conditions_ms =  T_CONDITIONS_MS()
        t_ext_cnd_tr    =  T_EXT_CND_TR()
        t_ext_cnd_ch_tr =  T_EXT_CND_CH_TR()
        t_url_ms        =  T_URL_MS()

    def getUrls(self, bland_cd='none'):
        if(bland_cd == 'none'):
            self.result = t_bland_ms.objects.all().values('access_url_string')
        else:
            self.result = url = t_bland_ms.objects.filter(bland_cd=self.bland_Cd).values('access_url_string')
        return self.result

if __name__ == "__main__":
    import pdb;pdb.set_trace()
    myscraper = MyScraper()
    myscraper.scrapeWebPage()
