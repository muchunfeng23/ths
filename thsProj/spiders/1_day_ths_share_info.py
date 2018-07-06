import scrapy
import time
from selenium import webdriver
from ..items import ShareEveryDayItem
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import random
from selenium.webdriver.common.proxy import *
import json

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

    def __init__(self,*args, **kwargs):
        self.agent_list = [\
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1",\
            "Mozilla/5.0 (X11; CrOS i686 2268.111.0) AppleWebKit/536.11 (KHTML, like Gecko) Chrome/20.0.1132.57 Safari/536.11",\
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1092.0 Safari/536.6",\
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.6 (KHTML, like Gecko) Chrome/20.0.1090.0 Safari/536.6",\
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/19.77.34.5 Safari/537.1",\
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.9 Safari/536.5",\
            "Mozilla/5.0 (Windows NT 6.0) AppleWebKit/536.5 (KHTML, like Gecko) Chrome/19.0.1084.36 Safari/536.5",\
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
            "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8_0) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1063.0 Safari/536.3",\
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1062.0 Safari/536.3",\
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
            "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
            "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.1 Safari/536.3",\
            "Mozilla/5.0 (Windows NT 6.2) AppleWebKit/536.3 (KHTML, like Gecko) Chrome/19.0.1061.0 Safari/536.3",\
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24",\
            "Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/535.24 (KHTML, like Gecko) Chrome/19.0.1055.1 Safari/535.24"
        ]
        pass

    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        browserGetProxys = webdriver.PhantomJS()
        browserGetProxys.get('http://47.106.180.108:8081/Index-generate_api_url.html?packid=2&fa=0&qty=97&port=1&format=json&ss=5&css=&ipport=1&et=1&pro=&city=')
        proxys = browserGetProxys.find_element_by_xpath('/html/body').text
        proxyObj = json.loads(proxys)
        allProxy = proxyObj["data"]
        ips = []
        for aProxy in allProxy[0:]:
            ips.append(aProxy["IP"])



        for i in range(1,30):

            proxyIp = ips[i+51].split(":")
            myIp = proxyIp[0]
            myPort = proxyIp[1]
            print(myIp,"    ---------------     ",myPort)
            # time.sleep(2)
            # if i % 3 == 1:
            #     browser.get("http://q.10jqka.com.cn/")
            #     browser.implicitly_wait(10)
            #     newCookie = browser.get_cookie("v")
            #     aCookies = browser.get_cookies()
            #     theCookie = {}
            #     for aCookie in aCookies[0:]:
            #         theCookie[aCookie["name"]] = aCookie["value"]
            #     print(theCookie)

            # ******************************************     phantomjs加agentlist  ****************************************
            # dcap = dict(DesiredCapabilities.PHANTOMJS)
            # dcap["phantomjs.page.settings.userAgent"] = random.choice(self.agent_list)
            # browser = webdriver.Firefox(desired_capabilities=dcap)
            # browser = webdriver.PhantomJS(desired_capabilities=dcap)

            # ***********************************************     phantomjs代理    ****************************************
            # browser = webdriver.PhantomJS()
            # proxy = webdriver.Proxy()
            # proxy.proxy_type = ProxyType.MANUAL
            # proxy.http_proxy = ips[i+20]
            # proxy.add_to_capabilities(webdriver.DesiredCapabilities.PHANTOMJS)
            # browser.start_session(webdriver.DesiredCapabilities.PHANTOMJS)

            # ************************************* 使用FireFox代理 ********************************************************
            profile = webdriver.FirefoxProfile()
            profile.set_preference("network.proxy.type", 1)
            profile.set_preference("network.proxy.http", myIp)
            profile.set_preference("network.proxy.http_port", int(myPort))
            profile.update_preferences()
            browser = webdriver.Firefox(profile)

            #***********************************************     chrome     ****************************************
            # chromedriver = "D:\\chromedriver\\chromedriver.exe"
            # options = webdriver.ChromeOptions()
            # options.add_experimental_option("excludeSwitches", ["ignore-certificate-errors"])
            # options.add_argument('--proxy-server=http://'+myIp+':'+myPort)
            # browser = webdriver.Chrome(chromedriver,chrome_options=options)
            # ****************************************************************************************************
            browser.implicitly_wait(30)
            browser.get("http://q.10jqka.com.cn/index/index/board/all/field/zdf/order/desc/page/" + str(i) + "/ajax/1/")

            print(browser.page_source)
            if len(browser.page_source) < 1000:
                browser.delete_all_cookies()
                browser.close()
                time.sleep(10)
                continue
            aTr = browser.find_element_by_xpath('/html/body/table/tbody/tr[1]').text
            browser.delete_all_cookies()
            browser.close()
            self.parseATr(aTr)
            print(aTr)
            time.sleep(10)
            pass

    def parseATr(self,trContent):
        item = ShareEveryDayItem()
        allTds = trContent.split(' ')
        print(len(allTds))
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
        item = shareData
        yield item


    # def parsePage(self,response):
    #     tbodyData = response.xpath('/html/body/table/tbody')
    #     allDatas = tbodyData.xpath('./tr')
    #     for aTrData in allDatas:
    #         item = ShareEveryDayItem()
    #         shareData = {}
    #         shareData["share_code"] = aTrData.xpath('./td[2]/a/text()').extract()[0]
    #         shareData["share_name"] = aTrData.xpath('./td[3]/a/text()').extract()[0]
    #         shareData["now_price"] = aTrData.xpath('./td[4]/text()').extract()[0]
    #         # 涨跌幅度
    #         shareData["rise_fall_ratio"] = aTrData.xpath('./td[5]/text()').extract()[0]
    #         # 涨跌
    #         shareData["rise_fall"] = aTrData.xpath('./td[6]/text()').extract()[0]
    #         # 涨速
    #         shareData["rise_speed"] = aTrData.xpath('./td[7]/text()').extract()[0]
    #         # 量比
    #         shareData["quantity_ratio"] = aTrData.xpath('./td[9]/text()').extract()[0]
    #         # 换手率
    #         shareData["exchange_radio"] = aTrData.xpath('./td[8]/text()').extract()[0]
    #         # 振幅，百分比
    #         shareData["amplitude"] = aTrData.xpath('./td[10]/text()').extract()[0]
    #         # 成交额
    #         turnover = aTrData.xpath('./td[11]/text()').extract()[0]
    #         if turnover.find("亿") > 0:
    #             shareData["turnover"] = float(turnover[0:len(turnover)-1]) * 100000000
    #         else:
    #             shareData["turnover"] = float(turnover[0: len(turnover) - 1]) * 10000
    #         # 流通股
    #         circulation_stock = aTrData.xpath('./td[12]/text()').extract()[0]
    #         shareData["circulation_stock_desc"] = circulation_stock
    #         if circulation_stock.find("亿") > 0:
    #             shareData["circulation_stock"] = float(circulation_stock[0:len(circulation_stock)-1])* 100000000
    #         else:
    #             shareData["circulation_stock"] = float(circulation_stock[0: len(circulation_stock) - 1]) * 10000
    #         # 流通市值
    #         circulation_value = aTrData.xpath('./td[13]/text()').extract()[0]
    #         shareData["circulation_value_desc"] = circulation_value
    #         if circulation_value.find("亿") > 0:
    #             shareData["circulation_value"] = float(circulation_value[0:len(circulation_value)-1]) * 100000000
    #         else:
    #             shareData["circulation_value"] = float(circulation_value[0: len(circulation_value) - 1]) * 10000
    #
    #         # 市盈率
    #         shareData["pe_ration"] = aTrData.xpath('./td[14]/text()').extract()[0]
    #         item = shareData
    #         yield item
