import scrapy
import MySQLdb
from scrapy.conf import settings
from selenium import webdriver
import time
from ..commvars import StrDate

class PlateData(scrapy.Spider):
    # 东方财富数据，行业资金流入数据
    name = "1_day_dfcf_industry_data"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.IndustryDataEveryDay': 200
        }
    }

    start_urls = ["http://www.baidu.com"]

    # http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKHY&sty=DCFFPBFM&st=(BalFlowMain)&sr=-1&p=1&ps=999&js=&token=894050c76af8597a853f5b408b759f5d&cb=callback009680662538759544&callback=callback009680662538759544&_=1554122386373
    def parse(self, response):
        request_url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKHY&sty=DCFFPBFM&st=(BalFlowMain)&sr=-1&p=1&ps=999&js=&token=894050c76af8597a853f5b408b759f5d&cb=callback009680662538759544&callback=callback009680662538759544&_=1554122386373"
        request = scrapy.Request(request_url,callback=self.parseData)
        yield request

    def parseData(self,response):
        # print(response.text)
        responseText = response.text
        indexLc = responseText.index("(")
        indexRc = responseText.index(")")
        print(indexLc," ",indexRc)
        tmp1 = responseText[indexLc+2:indexRc-1]
        tmp2 = tmp1.split("\",")
        now = StrDate.now()
        nowdate = now.datekey
        for tmp3 in tmp2:
            tmp4 = tmp3.replace("\"","").split(",")
            industryData = {}
            industryData["i_name"] = tmp4[2]
            industryData["amount"] = tmp4[3]
            industryData["datekey"] = nowdate
            yield industryData

