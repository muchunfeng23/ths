import scrapy
import time
from selenium import webdriver
from ..items import ShareEveryDayItem
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
from selenium.webdriver.common.proxy import *
import json
from pyvirtualdisplay import Display
from easyprocess import EasyProcess
from pyvirtualdisplay import Display
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions
import MySQLdb
from scrapy.conf import settings

class DFCF_share_info(scrapy.Spider):
    # 东方财富数据
    name = "1_day_dfcf_hq"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.ShareDataEveryDay': 200
        }
    }

    def __init__(self,*args, **kwargs):
        self.readMaxIndex()
        pass

    start_urls = ["http://www.baidu.com"]

    def readMaxIndex(self):
        conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        cursor = conn.cursor()
        cursor.execute("select max(index1) from crawler_share_everyday_data")
        # print("-----------",cursor.fetchone())
        self.maxIndex = cursor.fetchone()[0] + 1

    # http://quote.eastmoney.com/center/gridlist.html#hs_a_board
    def parse(self, response):
        for i in range(1,9):
            requestUrl = "http://nufm.dfcfw.com/EM_Finance2014NumericApplication/JS.aspx?cb=jQuery112404796567523005577_1534041330062&type=CT&token=4f1862fc3b5e77c150a2b985b12db0fd&sty=FCOIATC&js=(%7Bdata%3A%5B(x)%5D%2CrecordsFiltered%3A(tot)%7D)&cmd=C._A&st=(ChangePercent)&sr=-1&p="+str(i)+"&ps=500&_=1534041330064"
            request = scrapy.Request(requestUrl,self.parseAtr)
            yield request

    def parseAtr(self,response):
        allDataStr = str(response.body.decode("utf-8"))
        # print(allDataStr)
        indexFrom = allDataStr.index("(") + 1
        indexTo = allDataStr.index(")")
        jsonstr = allDataStr[indexFrom:indexTo]
        # print(jsonstr)
        # jsonstr = jsonstr.replace('pages','"pages"')
        # jsonstr = jsonstr.replace('date','"date"')
        jsonstr = jsonstr.replace('data', '"data"')
        jsonstr = jsonstr.replace('recordsFiltered','"recordsFiltered"')
        allJsonData = json.loads(jsonstr, strict=False)
        allData = allJsonData["data"]
        for aData in allData:
            print(aData)
            allTds = aData.split(",")
            print(allTds[0]," ",allTds[2])

            shareData = {}
            shareData["share_code"] = allTds[1]
            shareData["share_name"] = allTds[2]
            shareData["now_price"] = allTds[3]
            # 涨跌幅度
            shareData["rise_fall_ratio"] = allTds[5]
            # 涨跌
            shareData["rise_fall"] = allTds[4]
            # 量比
            shareData["quantity_ratio"] = allTds[13]
            # 换手率
            shareData["exchange_radio"] = allTds[14]
            # 振幅，百分比
            shareData["amplitude"] = allTds[7]
            # 成交额
            shareData["turnover"] = allTds[6]
            # 市盈率
            shareData["pe_ration"] = allTds[15]
            shareData["newIndex"] = self.maxIndex
            yield shareData
