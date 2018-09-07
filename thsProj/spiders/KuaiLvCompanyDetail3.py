import scrapy
import json
from ..items import DataItem
import MySQLdb
from scrapy.conf import settings

class newSpider(scrapy.Spider):
    name = "kuailvCompanyDetail"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.KuaiLvCompanyDetail': 200
        }
    }

    def __init__(self,*args, **kwargs):
        self.readAllKpIds()
        pass

    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        for aPoiId in self.allPoiId:
            print("===============",aPoiId)
            poiId = aPoiId[0]
            requestUrl = "https://klcrm.meituan.com/crm/app/poi/r/getPoi?poiId="+poiId+"&ua=30402_ios&token=d7e567f07c*644b4896e6ec8c2bb6983"
            print("requestUrl = ",requestUrl)
            request = scrapy.Request(requestUrl, self.parseData)
            request.meta["poiId"] = poiId
            yield request

    def parseData(self,response):
        target_json = json.loads(response.body.decode("utf-8"))
        detail = target_json['data']
        data = {}
        data["alldata"] = detail
        data["poiId"] = response.meta["poiId"]
        data["latitude"] = detail["latitude"]
        data["longitude"] = detail["longitude"]
        raw_item = data
        yield raw_item

    def readAllKpIds(self):
        conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        cursor = conn.cursor()
        cursor.execute("select poiId from z_kuailv_seller_company_info_all")
        self.allPoiId = list(cursor.fetchall())
        print(self.allPoiId)