import scrapy
import MySQLdb
from scrapy.conf import settings
from selenium import webdriver
import time
from ..commvars import StrDate

class ConceptData(scrapy.Spider):
    # 东方财富数据，行业资金流入数据
    name = "1_day_dfcf_concept_data"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.ConceptDataEveryDay': 200
        }
    }

    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        request_url = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?type=CT&cmd=C._BKGN&sty=DCFFPBFM&st=(BalFlowMain)&sr=-1&p=1&ps=10000&js=&token=894050c76af8597a853f5b408b759f5d&cb=callback08792277980038559&callback=callback08792277980038559&_=1554125415315"
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
            industryData["c_name"] = tmp4[2]
            industryData["amount"] = tmp4[3]
            industryData["datekey"] = nowdate
            yield industryData

