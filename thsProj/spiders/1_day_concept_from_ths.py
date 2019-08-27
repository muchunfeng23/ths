import scrapy
import time
from selenium import webdriver
from ..items import ConceptFromThsItem
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

# 每日读取同花顺的所有股票信息，包括价格，量比，等信息，已不可使用

from scrapy.conf import settings

class THS_share_info(scrapy.Spider):
    name = "1_day_concept_ths"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.ConceptFromThs': 200
        }
    }

    def __init__(self,*args, **kwargs):
        self.readMaxIndex()
        pass

    start_urls = ["http://www.baidu.com"]


    def parse(self, response):
        browser = webdriver.Firefox()
        # browser = webdriver.phantomjs()
        browser.get('http://data.10jqka.com.cn/funds/gnzjl/#')
        # WebDriverWait(browser,10).until(expected_conditions.visibility_of_element_located((By.TAG_NAME,'tbody')))
        pageNum = 0;
        try:
            while pageNum < 6:
                tbody = browser.find_element_by_xpath('//*[@id="J-ajax-main"]/table/tbody').text
                allTrs = tbody.split('\n')
                paihangInPage = 0;
                for aTr in allTrs[0:]:
                    print(aTr)
                    paihangInPage += 1
                    item = ConceptFromThsItem()
                    allTds = aTr.split(' ')
                    conceptData = {}
                    conceptData["hangye1"] = allTds[1]
                    print("行业 = " + conceptData["hangye1"])
                    conceptData["hangyezhishu"] = allTds[2]
                    conceptData["zhangdiefu"] = allTds[3][:-1]
                    conceptData["liuruzijin"] = allTds[4]
                    conceptData["liuchuzijin"] = allTds[5]
                    conceptData["jiner"] = allTds[6]
                    conceptData["mainshare"] = allTds[8]
                    conceptData["mainshareup"] = allTds[9][:-1]
                    conceptData["dayIndex"] = self.maxIndex
                    conceptData["paihangIndex"] = pageNum * 50 + paihangInPage
                    item = conceptData
                    yield item
                time.sleep(6)
                nextPage = browser.find_element_by_link_text("下一页")
                nextPage.click()
                pageNum = pageNum + 1
            browser.close()
        except Exception as err:
            print(err)
            browser.close()

    def readMaxIndex(self):
        conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        cursor = conn.cursor()
        cursor.execute("select max(dayIndex) from ths_concept_everyday")
        adata = cursor.fetchone()[0]
        # print("read max = " + str(cursor.fetchone()[0] is None))
        if(adata is None):
            self.maxIndex = 1
        else:
            print("cursor.fetchone()[0] = " , adata)
            self.maxIndex = adata + 1


