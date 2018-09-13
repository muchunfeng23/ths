import scrapy
import json
from ..items import DataItem
import MySQLdb
from scrapy.conf import settings

class newSpider(scrapy.Spider):
    name = "kuailvCompanyOrderList"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.KuaiLvCompanyOrderList': 200
        }
    }

    def __init__(self,*args, **kwargs):
        self.readAllPoiIds()
        pass

    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        for aPoiId in self.allPoiId:
            poiId = aPoiId[0]
            # 获取订单列表
            requestUrl = "https://klcrm.meituan.com/crm/app/order/r/orderList?pageNo=1&pageSize=20&statusList=DELIVERED%2CCOMPLETED&poiId="+poiId+"&ua=30402_ios&token=d7e567f07c*644b4896e6ec8c2bb6983"
            # print("requestUrl = ",requestUrl)
            request = scrapy.Request(requestUrl, self.parseData)
            request.meta["poiId"] = poiId
            yield request

    def parseData(self,response):
        target_json = json.loads(response.body.decode("utf-8"))
        # 处理第一页，处理所有的订单
        allData = target_json["data"]["pageContent"]
        for aData in allData:
            orderid = aData["id"]
            requestUrl = "https://klcrm.meituan.com/oms/api/v1/order/r/detail?orderId="+str(orderid)+"&ua=30402_ios&token=d7e567f07c*644b4896e6ec8c2bb6983"
            request = scrapy.Request(requestUrl, self.saveData)
            request.meta["orderid"] = orderid
            request.meta["poiId"] = response.meta["poiId"]
            yield request

        # 处理多的页面
        pageSize = target_json["data"]["page"]["totalPageCount"]
        for pageIndex in range(2,pageSize + 1):
            requestUrl = "https://klcrm.meituan.com/crm/app/order/r/orderList?pageNo="+str(pageIndex)+"&pageSize=20&statusList=DELIVERED%2CCOMPLETED&poiId=10336977&ua=30402_ios&token=d7e567f07c*644b4896e6ec8c2bb6983"
            request = scrapy.Request(requestUrl, self.saveData)
            request.meta["orderid"] = orderid
            request.meta["poiId"] = response.meta["poiId"]
            yield request


    def saveData(self,response):
        target_json = json.loads(response.body.decode("utf-8"))
        orderDetail = {}
        orderDetail["orderid"] = response.meta["orderid"]
        # orderDetail["poiId"] = target_json["data"]["order"]["userId"]
        orderDetail["poiId"] = response.meta["poiId"]
        orderDetail["ctime"] = target_json["data"]["order"]["ctime"]
        orderDetail["alldata"] = target_json["data"]
        print("======================== ",orderDetail)
        yield orderDetail

    def readAllPoiIds(self):
        conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        cursor = conn.cursor()
        cursor.execute("select poiId from z_kuailv_seller_company_info_all")
        self.allPoiId = list(cursor.fetchall())
        print(self.allPoiId)