import scrapy
import json
from ..items import DataItem
class newSpider(scrapy.Spider):
    name = "kuailvXiaoShou"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.KuaiLvSellCompanyInfo': 200
        }
    }

    def __init__(self,*args, **kwargs):
        pass

    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        longitudeFrom = 117.65
        longitudeTo = 118.00
        latitudeFrom = 39.13
        latitudeTo = 40.00

        longitudeSpace = 0.07
        latitudeSpace = 0.045
        longitudeSize = int((longitudeTo - longitudeFrom)/longitudeSpace) + 1
        latitudeSize = int((latitudeTo - latitudeFrom)/latitudeSpace) + 1
        for longitudeIndex in range(1,longitudeSize):
            for latitudeIndex in range(1,latitudeSize):
                nowLongitude = longitudeFrom + longitudeSpace * longitudeIndex
                nowLatitude = latitudeFrom + latitudeSpace * latitudeIndex
                print("nowLongitude = ",nowLongitude," nowLatitude = ",nowLatitude)
                requestUrl = "https://klcrm.meituan.com/crm/app/poi/r/allList?pageNo=1&latitude="+str(nowLatitude)+"&longitude="+str(nowLongitude)+"&pageSize=500&cat1Id=&cat2Id=&sortType=THREE_KM&onlineStatus=DEFAULT&poiBelongStatus=&ua=30402_ios&token=d7e567f07c*644b4896e6ec8c2bb6983"
                request = scrapy.Request(requestUrl, self.parseData)
                request.meta['longitude'] = str(nowLongitude)
                request.meta['latitude'] = str(nowLatitude)
                yield request

    def parseData(self,response):
        target_json = json.loads(response.body.decode("utf-8"))
        allCompany = target_json['data']['pageContent']
        for aCompany in allCompany:
            raw_item = DataItem()
            raw_item = aCompany
            yield raw_item
        #
        nowLongitude = response.meta['longitude']
        nowLatitude = response.meta['latitude']
        # print(target_json)
        allPageSize = target_json['data']['page']['totalPageCount']
        for pageIndex in range(2,allPageSize):
            print("nowLatitude=",nowLatitude,"nowLongitude=",nowLongitude)
            requestUrl = "https://klcrm.meituan.com/crm/app/poi/r/allList?pageNo="\
                         +str(pageIndex)+"&latitude="+nowLatitude+"&longitude="+nowLongitude+"&pageSize=500&cat1Id=&cat2Id=&sortType=THREE_KM&onlineStatus=DEFAULT&poiBelongStatus=&ua=30402_ios&token=d7e567f07c*644b4896e6ec8c2bb6983"
            request = scrapy.Request(requestUrl, self.saveData)
            yield request


    def saveData(self,response):
        target_json = json.loads(response.body.decode("utf-8"))
        allCompany = target_json['data']['pageContent']
        for aCompany in allCompany:
            raw_item = DataItem()
            raw_item = aCompany
            yield raw_item
