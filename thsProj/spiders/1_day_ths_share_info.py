import scrapy
import time
from selenium import webdriver
from ..items import ShareEveryDayItem

class THS_share_info(scrapy.Spider):
    name = "1_day_share_info_everyday"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.ShareDataEveryDay': 200
        }
    }

    def __init__(self):
        self.agent_list = USER_AGENT_LIST = [
            'Mozilla/5.0 (iPhone; CPU iPhone OS 9_3_4 like Mac OS X) AppleWebKit/601.1.46 (KHTML, like Gecko) Mobile/13G35 MicroMessenger/6.3.23 NetType/WIFI Language/en']
        pass

    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        # browser = webdriver.Firefox()
        browser = webdriver.PhantomJS()
        newCookie = ""
        for i in range(1,164):
            time.sleep(2)
            if i % 3 == 1:
                browser.get("http://q.10jqka.com.cn/")
                browser.implicitly_wait(10)
                newCookie = browser.get_cookie("v")
                print(newCookie["value"])
            request = scrapy.Request(
                "http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/" + str(i) + "/ajax/1/",
                cookies={"__utma": "156575163.293155705.1529204448.1529204448.1529204448.1",
                         "__utmc": "156575163",
                         "__utmz": "156575163.1529204448.1.1.utmcsr=master.10jqka.com.cn|utmccn=(referral)|utmcmd=referral|utmcct=/20180615/c605104296.shtml",
                         "escapename": "%25u6768%25u6c90%25u98ce",
                         "ticket": "86b96e6ced2658f3e5ab822ef5a767c9",
                         "Hm_lvt_78c58f01938e4d85eaf619eae71b4ed1": "1528249821,1528940841,1529201959,1529219313",
                         "Hm_lpvt_78c58f01938e4d85eaf619eae71b4ed1": "1529219816",
                         "td_cookie": "18446744070881521119",
                         "v": newCookie["value"]},
                callback=self.parsePage)
            yield request
        browser.close()

        # phantomJsDir = "D:/plantomjs/phantomjs-2.1.1-windows/bin/phantomjs.exe"
        # browser = webdriver.PhantomJS(phantomJsDir)
        # ****************************************************************************************************************
        # ****搞了半天原来是浏览器引擎PhantomJS不支持click操作造成的*
        # ****************************************************************************************************************
        # browser = webdriver.PhantomJS()


        # **********************************  因为页面会自动刷新，引入了一些不好解决的问题，所以selenium的click暂时先不用 *************************************
        # browser = webdriver.Firefox()
        # browser.get("http://q.10jqka.com.cn/")
        # browser.implicitly_wait(10)
        # myCookie = browser.get_cookie("v")
        # print("myCookie = ",myCookie)
        # while True:
        #     trContents = browser.find_elements_by_xpath('//*[@id="maincont"]/table/tbody/tr')
        #     for i in range(0,len(trContents)):
        #         trData = trContents[i]
        #         aTrDts = trData.text.split(" ")
        #         print(aTrDts[2])
        #     # nextPage = browser.find_element_by_xpath('//*[@id="m-page"]/a[5]')
        #     nextPage = browser.find_element_by_link_text("下一页")
        #     if type(nextPage) == None:
        #         break
        #     nextPage.click()
        #     time.sleep(0.2)



    def parsePage(self,response):
        tbodyData = response.xpath('/html/body/table/tbody')
        allDatas = tbodyData.xpath('./tr')
        for aTrData in allDatas:
            item = ShareEveryDayItem()
            shareData = {}
            shareData["share_code"] = aTrData.xpath('./td[2]/a/text()').extract()[0]
            shareData["share_name"] = aTrData.xpath('./td[3]/a/text()').extract()[0]
            shareData["now_price"] = aTrData.xpath('./td[4]/text()').extract()[0]
            # 涨跌幅度
            shareData["rise_fall_ratio"] = aTrData.xpath('./td[5]/text()').extract()[0]
            # 涨跌
            shareData["rise_fall"] = aTrData.xpath('./td[6]/text()').extract()[0]
            # 涨速
            shareData["rise_speed"] = aTrData.xpath('./td[7]/text()').extract()[0]
            # 量比
            shareData["quantity_ratio"] = aTrData.xpath('./td[9]/text()').extract()[0]
            # 换手率
            shareData["exchange_radio"] = aTrData.xpath('./td[8]/text()').extract()[0]
            # 振幅，百分比
            shareData["amplitude"] = aTrData.xpath('./td[10]/text()').extract()[0]
            # 成交额
            turnover = aTrData.xpath('./td[11]/text()').extract()[0]
            if turnover.find("亿") > 0:
                shareData["turnover"] = float(turnover[0:len(turnover)-1]) * 100000000
            else:
                shareData["turnover"] = float(turnover[0: len(turnover) - 1]) * 10000
            # 流通股
            circulation_stock = aTrData.xpath('./td[12]/text()').extract()[0]
            shareData["circulation_stock_desc"] = circulation_stock
            if circulation_stock.find("亿") > 0:
                shareData["circulation_stock"] = float(circulation_stock[0:len(circulation_stock)-1])* 100000000
            else:
                shareData["circulation_stock"] = float(circulation_stock[0: len(circulation_stock) - 1]) * 10000
            # 流通市值
            circulation_value = aTrData.xpath('./td[13]/text()').extract()[0]
            shareData["circulation_value_desc"] = circulation_value
            if circulation_value.find("亿") > 0:
                shareData["circulation_value"] = float(circulation_value[0:len(circulation_value)-1]) * 100000000
            else:
                shareData["circulation_value"] = float(circulation_value[0: len(circulation_value) - 1]) * 10000

            # 市盈率
            shareData["pe_ration"] = aTrData.xpath('./td[14]/text()').extract()[0]
            item = shareData
            yield item
