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

        now = StrDate.now()
        nowdate = now.datekey
        conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        conn.autocommit(True)
        cursor = conn.cursor()
        browser = webdriver.Firefox()
        browser.implicitly_wait(10)
        for shareCodeNum in range(len(self.allShares)):
            # browser = webdriver.PhantomJS()

            print("share_code = ",self.allShares[shareCodeNum][0])
            aShareCode = self.allShares[shareCodeNum][0]
            i = 0
            browser.get("http://quotes.money.163.com/trade/ddtj_"+aShareCode+","+str(i)+".html?amount=100000")
            try:
                trs1 = browser.find_element_by_xpath('//*[@id="infoPanel"]/table/tbody/tr[1]').text.split(" ")
                trs2 = browser.find_element_by_xpath('//*[@id="infoPanel"]/table/tbody/tr[2]').text.split(" ")
                avg_price = trs1[2].split("：")[1].replace("元","")
                big_sum_trade_num = trs1[0].split("：")[1].replace("手","").replace(",","")
                sum_trade_num = trs2[0].split("：")[1].replace("手","").replace(",","")
                big_buy_num = trs1[3].split("：")[1].replace("手","").replace(",","")
                big_sell_num = trs2[2].split("：")[1].replace("手","").replace(",","")
                # print("================",aShareCode,"#", avg_price,"#", big_sum_trade_num,"#", sum_trade_num,"#", big_buy_num, "#",big_sell_num,"#", nowdate)
                print(aShareCode, avg_price, big_sum_trade_num, sum_trade_num, big_buy_num, big_sell_num, nowdate)
                cursor.execute('insert into crawler_big_bill_records (share_code, avg_price, big_sum_trade_num, sum_trade_num, big_buy_num, big_sell_num, datekey) values(%s,%s,%s,%s,%s,%s,%s)'
                                %(aShareCode, avg_price, big_sum_trade_num, sum_trade_num, big_buy_num, big_sell_num, nowdate))

            except Exception as err1:
                print(err1)
                browser.close()
                break
            i += 1
            pass
        browser.close()
        cursor.close()
        conn.close()





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

        now = StrDate.now()
        nowdate = now.datekey
        conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        conn.autocommit(True)
        cursor = conn.cursor()
        browser = webdriver.Firefox()
        browser.implicitly_wait(10)
        for shareCodeNum in range(len(self.allShares)):
            # browser = webdriver.PhantomJS()

            print("share_code = ",self.allShares[shareCodeNum][0])
            aShareCode = self.allShares[shareCodeNum][0]
            i = 0
            browser.get("http://quotes.money.163.com/trade/ddtj_"+aShareCode+","+str(i)+".html?amount=100000")
            try:
                trs1 = browser.find_element_by_xpath('//*[@id="infoPanel"]/table/tbody/tr[1]').text.split(" ")
                trs2 = browser.find_element_by_xpath('//*[@id="infoPanel"]/table/tbody/tr[2]').text.split(" ")
                avg_price = trs1[2].split("：")[1].replace("元","")
                big_sum_trade_num = trs1[0].split("：")[1].replace("手","").replace(",","")
                sum_trade_num = trs2[0].split("：")[1].replace("手","").replace(",","")
                big_buy_num = trs1[3].split("：")[1].replace("手","").replace(",","")
                big_sell_num = trs2[2].split("：")[1].replace("手","").replace(",","")
                # print("================",aShareCode,"#", avg_price,"#", big_sum_trade_num,"#", sum_trade_num,"#", big_buy_num, "#",big_sell_num,"#", nowdate)
                print(aShareCode, avg_price, big_sum_trade_num, sum_trade_num, big_buy_num, big_sell_num, nowdate)
                cursor.execute('insert into crawler_big_bill_records (share_code, avg_price, big_sum_trade_num, sum_trade_num, big_buy_num, big_sell_num, datekey) values(%s,%s,%s,%s,%s,%s,%s)'
                                %(aShareCode, avg_price, big_sum_trade_num, sum_trade_num, big_buy_num, big_sell_num, nowdate))

            except Exception as err1:
                print(err1)
                browser.close()
                break
            i += 1
            pass
        browser.close()
        cursor.close()
        conn.close()





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



