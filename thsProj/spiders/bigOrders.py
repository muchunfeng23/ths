import scrapy
import MySQLdb
from scrapy.conf import settings
from selenium import webdriver
import time
from ..commvars import StrDate

class BigOrder(scrapy.Spider):
    name="big_orders"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.BigOrdersEveryDay': 200
        }
    }

    def __init__(self, *args, **kwargs):
        self.readAllShares()
        pass

    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        now = StrDate.now()
        nowdate = now.datekey
        browser = webdriver.PhantomJS()
        browser.implicitly_wait(10)
        for shareCode in self.allShares:
            try:
                orderUrl = "http://quotes.money.163.com/trade/ddtj_"+str(shareCode[0])+".html"
                browser.get(orderUrl)
                bigAmount = browser.find_element_by_xpath('//*[@id="infoPanel"]/table/tbody/tr[1]/td[1]/span').text.replace(",","").replace("手","")
                sumAmount = browser.find_element_by_xpath('//*[@id="infoPanel"]/table/tbody/tr[2]/td[1]/span').text.replace(",","").replace("手","")
                avgPrice = browser.find_element_by_xpath('//*[@id="infoPanel"]/table/tbody/tr[1]/td[3]/span').text.replace(",","").replace("元","")
                mainBuy = browser.find_element_by_xpath('//*[@id="infoPanel"]/table/tbody/tr[1]/td[4]/span').text.replace(",","").replace("手","")
                mainSell = browser.find_element_by_xpath('//*[@id="infoPanel"]/table/tbody/tr[2]/td[4]/span').text.replace(",","").replace("手","")
                print(bigAmount , " " ,sumAmount ," ",avgPrice," ",mainBuy," ",mainSell)
                shareData = {}
                shareData["share_code"] = str(shareCode[0])
                shareData["sum_amount"] = sumAmount
                shareData["big_amount"] = bigAmount
                shareData["big_buy"] = mainBuy
                shareData["big_sell"] = mainSell
                shareData["big_avg_price"] = avgPrice
                shareData["datekey"] = nowdate
                yield shareData
            except Exception as error:
                print(error)
            time.sleep(0.2)
        browser.close()


    def readAllShares(self):
        conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        cursor = conn.cursor()
        cursor.execute("select share_code from all_shares")
        self.allShares = list(cursor.fetchall())
        print(self.allShares)
