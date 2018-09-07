import scrapy
import json
from ..items import DataItem
import time
import random
import MySQLdb
from scrapy.conf import settings

class newSpider(scrapy.Spider):
    name = "kuailvKpiTelephone"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.KuaiLvKpidTelephone': 200
        }
    }

    def __init__(self,*args, **kwargs):
        self.readAllKpIds()
        pass

    start_urls = ["http://www.baidu.com"]

    def parse(self,response):
        for aKpId in self.allKpIds:
            kpId = aKpId[0]
            requestUrl = "https://klcrm.meituan.com/crm/app/contact/r/contactTel?id="+str(kpId)+"&ua=30402_ios&token=d7e567f07c*644b4896e6ec8c2bb6983"
            print("---------- ",requestUrl,"   ",kpId)
            request = scrapy.Request(requestUrl, self.saveData)
            request.meta['kpId'] = kpId
            # time.sleep(random.randint(2,8))
            yield request


    def saveData(self,response):
        target_json = json.loads(response.body.decode("utf-8"))
        aTelephone = target_json['data']
        kpId = response.meta["kpId"]
        print("-----------------aTelephone = ",aTelephone)
        raw_item = DataItem()
        allData = {}
        allData["kpid"] = kpId
        allData["telephone"] = aTelephone
        raw_item = allData
        yield raw_item

    def readAllKpIds(self):
        conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        cursor = conn.cursor()
        cursor.execute("select kpId from z_kuailv_seller_company_info_all")
        self.allKpIds = list(cursor.fetchall())
        print(self.allKpIds)
