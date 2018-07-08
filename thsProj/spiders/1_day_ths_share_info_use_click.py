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

class THS_share_info(scrapy.Spider):
    name = "1_day_share_info_everyday_use_click"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.ShareDataEveryDay': 200
        }
    }

    def __init__(self,*args, **kwargs):
        pass

    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        display = Display(visible=0, size=(1024, 768))
        display.start()
        browser = webdriver.Firefox()
        browser.get('http://q.10jqka.com.cn/')
        WebDriverWait(browser,10).until(expected_conditions.visibility_of_element_located((By.TAG_NAME,'tbody')))
        clickTimes = 0
        while clickTimes < 166:
            try:
                tbody = browser.find_element_by_xpath('//*[@id="maincont"]/table/tbody').text
                allTrs = tbody.split('\n')
                for aTr in allTrs[0:]:
                    print(aTr," --------------- clicktimes = ",clickTimes)
                    item = ShareEveryDayItem()
                    shareData = self.parseAtr(aTr)
                    item = shareData
                    yield item
                    # raise Exception("抛出一个异常")
                nextPage = browser.find_element_by_link_text("下一页")
                nextPage.click()
                clickTimes += 1
            except Exception as err:
                print(err)
                if clickTimes == 165:
                    break
                self.toRefresh(browser, clickTimes)
                continue
        display.stop()


    def parseAtr(self,aTr):
        allTds = aTr.split(' ')
        shareData = {}
        shareData["share_code"] = allTds[1]
        shareData["share_name"] = allTds[2]
        shareData["now_price"] = allTds[3]
        # 涨跌幅度
        shareData["rise_fall_ratio"] = allTds[4]
        # 涨跌
        shareData["rise_fall"] = allTds[5]
        # 涨速
        shareData["rise_speed"] = allTds[6]
        # 量比
        shareData["quantity_ratio"] = allTds[8]
        # 换手率
        shareData["exchange_radio"] = allTds[7]
        # 振幅，百分比
        shareData["amplitude"] = allTds[9]
        # 成交额
        turnover = allTds[10]
        if turnover.find("亿") > 0:
            shareData["turnover"] = float(turnover[0:len(turnover) - 1]) * 100000000
        else:
            shareData["turnover"] = float(turnover[0: len(turnover) - 1]) * 10000
        # 流通股
        circulation_stock = allTds[11]
        shareData["circulation_stock_desc"] = circulation_stock
        if circulation_stock.find("亿") > 0:
            shareData["circulation_stock"] = float(circulation_stock[0:len(circulation_stock) - 1]) * 100000000
        else:
            shareData["circulation_stock"] = float(circulation_stock[0: len(circulation_stock) - 1]) * 10000
        # 流通市值
        circulation_value = allTds[12]
        shareData["circulation_value_desc"] = circulation_value
        if circulation_value.find("亿") > 0:
            shareData["circulation_value"] = float(circulation_value[0:len(circulation_value) - 1]) * 100000000
        else:
            shareData["circulation_value"] = float(circulation_value[0: len(circulation_value) - 1]) * 10000
        # 市盈率
        shareData["pe_ration"] = allTds[13]
        return shareData

    def toRefresh(self,browser,clickTimes):
        browser.refresh()
        browser.get('http://q.10jqka.com.cn/')
        fanye = 1
        nextFy = 5 * fanye
        while (nextFy <= clickTimes + 1):
            spacePage = browser.find_element_by_link_text(str(5 * fanye))
            spacePage.click()
            time.sleep(1)
            nextPage = browser.find_element_by_link_text("下一页")
            nextPage.click()
            time.sleep(1)
            fanye += 1
            nextFy = 5 * fanye
            continue
        getRightPage = browser.find_element_by_link_text(str(clickTimes + 1))
        clickTimes += 1
        getRightPage.click()