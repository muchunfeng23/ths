import scrapy
from selenium import webdriver
import MySQLdb
from scrapy.conf import settings
from ..commvars import StrDate

class BigNum(scrapy.Spider):
    name = "1_day_stastic_big_num"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.ThsprojPipeline': 200
        }
    }

    start_urls = ["http://www.baidu.com"]

    def __init__(self):
        self.readAllShares()
        pass

    def parse(self, response):
        browser = webdriver.PhantomJS()
        browser.implicitly_wait(10)
        now = StrDate.now()
        nowdate = now.datekey
        for shareCodeNum in range(len(self.allShares)):
            print("share_code = ",self.allShares[shareCodeNum][0])
            aShareCode = self.allShares[shareCodeNum][0]
            i = 0
            while True:
                browser.get("http://quotes.money.163.com/trade/ddtj_"+aShareCode+","+str(i)+".html?amount=500000")
                try:
                    trs1 = browser.find_element_by_xpath('//*[@id="dadanTable"]/div[1]/div/table/tbody').text
                except Exception as err1:
                    print(err1)
                    break
                trs1Array = trs1.split('\n')
                values1 = []
                for trContent in trs1Array[0:]:
                    tdContents = trContent.split(' ')
                    values1.append((aShareCode,tdContents[0],tdContents[1],tdContents[2],tdContents[3],tdContents[4],nowdate))
                print(values1)
                self.batchInsert(values1)
                try:
                    trs2 = browser.find_element_by_xpath('//*[@id="dadanTable"]/div[2]/div/table/tbody').text
                except Exception as err2:
                    print(err2)
                    break
                trs2Array = trs2.split('\n')
                values2 = []
                for trContent in trs2Array[0:]:
                    tdContents = trContent.split(' ')
                    values2.append((aShareCode, tdContents[0], tdContents[1], tdContents[2], tdContents[3],
                                    tdContents[4], nowdate))
                self.batchInsert(values2)

                i += 1
                pass


        pass

    def batchInsert(self,values):
        conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        conn.autocommit(True)
        cursor = conn.cursor()
        cursor.executemany('insert into crawler_big_bill_records (share_code,trade_time,price,trade_quantity,trade_money,trade_property,datekey) values(%s,%s,%s,%s,%s,%s,%s)',values)
                           # %(values[0],values[1],values[2],values[3],values[4],values[5],values[6]))
        cursor.close()
        conn.close()
        pass

    def readAllShares(self):
        conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        cursor = conn.cursor()
        cursor.execute("select share_code from all_shares")
        self.allShares = list(cursor.fetchall())
        print(self.allShares)



