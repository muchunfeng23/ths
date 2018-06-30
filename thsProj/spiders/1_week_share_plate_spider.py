import scrapy
from ..items import DataItem
import time
from selenium import webdriver

class SharePlateInfo(scrapy.Spider):
    name = "1_week_share_plate_spider"
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.SharePlateData': 200
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
        for i in range(1, 164):
            time.sleep(3)
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

    def parsePage(self,response):
        tbodyData = response.xpath('/html/body/table/tbody')
        allDatas = tbodyData.xpath('./tr')
        for aTrData in allDatas:
            shareCode = aTrData.xpath('./td[2]/a/text()').extract()[0]
            request2 = scrapy.Request("http://basic.10jqka.com.cn/"+shareCode+"/concept.html",callback=self.parsePlate)
            request2.meta["shareCode"] = shareCode
            # r = requests.get("http://basic.10jqka.com.cn/"+shareCode+"/concept.html")
            # result = r.content.decode("utf-8")
            yield request2

    def parsePlate(self,response):
        allPlates = response.xpath('//*[@id="concept"]/div[2]/div/table/tbody/tr')
        # //*[@id="concept"]/div[2]/div/table/tbody/tr[1]/td[2]
        for i in range(0, len(allPlates), 2):
            aTr = allPlates[i]
            aTrDesc = allPlates[i + 1]
            item = DataItem()
            plate = {}

            plate["share_code"] = response.meta["shareCode"]
            platNameInfo = aTr.xpath('./td[2]/text()').extract()[0]
            if platNameInfo.find("<a") > 0:
                indexOfA = platNameInfo.index("<a")
                tmpInfo = platNameInfo[0:indexOfA]
                realInfo = tmpInfo.replace('"', '').replace("\n", "").replace("\t", "").replace(" ", "").replace("\xa0","").replace("\\","")
                plate["plate_name"] = realInfo
            else:
                plate["plate_name"] = platNameInfo.replace('"', '').replace("\n", "").replace("\t", "").replace(" ", "").replace("\xa0","").replace("\\","")
            try:
                desc = aTrDesc.xpath('./td/div/text()').extract()[1].replace("\n", "").replace("\t", "").replace(" ", "").replace("\xa0","").replace("\\","").replace("\"","'")
                plate["desc"] = desc
            except Exception:
                plate["desc"] = ""
                pass
            item = plate
            yield item