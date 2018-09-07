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
        # longitudes = [
        #     "117.168157",
        #     "117.165007",
        #     "117.187876",
        #     "117.146736",
        #     "117.202736",
        #     "117.206535",
        #     "117.212041",
        #     "117.220328",
        #     "117.232478",
        #     "117.184823",
        #     "117.186725",
        #     "117.197225",
        #     "117.200687",
        #     "117.215061",
        #     "117.21674",
        #     "117.212751",
        #     "117.260912",
        #     "117.261668",
        #     "117.27223",
        #     "117.270884",
        #     "117.270533",
        #     "117.213245",
        #     "117.20808",
        #     "117.209437",
        #     "117.22151",
        #     "117.208738",
        #     "117.203287",
        #     "117.284789",
        #     "117.686258",
        #     "117.688162",
        #     "117.691285",
        #     "117.693368",
        #     "117.703594",
        #     "117.687746",
        #     "117.689685",
        #     "117.692971",
        #     "117.695081",
        #     "117.696641",
        #     "117.702398",
        #     "117.711538",
        #     "117.690724",
        #     "117.707991",
        #     "117.731575",
        #     "117.199344",
        #     "117.188156",
        #     "117.21747",
        #     "117.211166",
        #     "117.246617",
        #     "117.206178",
        #     "117.19746",
        #     "117.180526",
        #     "117.178254",
        #     "117.195007",
        #     "117.175215",
        #     "117.352678",
        #     "117.169551"
        # ]
        # latitudes = [
        #     "39.185547",
        #     "39.175857",
        #     "39.151716",
        #     "39.143245",
        #     "39.160004",
        #     "39.163545",
        #     "39.167913",
        #     "39.171914",
        #     "39.172582",
        #     "39.217873",
        #     "39.215218",
        #     "39.202807",
        #     "39.199283",
        #     "39.194261",
        #     "39.189493",
        #     "39.185457",
        #     "39.130593",
        #     "39.116275",
        #     "39.115835",
        #     "39.11302",
        #     "39.107072",
        #     "39.136691",
        #     "39.131308",
        #     "39.12843",
        #     "39.121619",
        #     "39.123004",
        #     "39.127534",
        #     "39.066967",
        #     "39.035491",
        #     "39.035111",
        #     "39.034494",
        #     "39.034155",
        #     "39.030444",
        #     "39.039633",
        #     "39.038795",
        #     "39.038297",
        #     "39.037916",
        #     "39.037385",
        #     "39.035364",
        #     "39.032081",
        #     "39.043345",
        #     "39.037871",
        #     "39.029146",
        #     "39.149187",
        #     "39.147301",
        #     "39.144999",
        #     "39.14077",
        #     "39.115768",
        #     "39.16765",
        #     "39.156767",
        #     "39.138299",
        #     "39.152241",
        #     "39.151679",
        #     "39.109358",
        #     "38.994944",
        #     "39.116067"
        # ]
        # for zuobiaoIndex in range(0,len(longitudes)):
        #     requestUrl = "https://klcrm.meituan.com/crm/app/poi/r/allList?pageNo=1&latitude=" + latitudes[zuobiaoIndex] + "&longitude=" + longitudes[zuobiaoIndex] + "&pageSize=500&cat1Id=&cat2Id=&sortType=THREE_KM&onlineStatus=DEFAULT&poiBelongStatus=&ua=30402_ios&token=d7e567f07c*644b4896e6ec8c2bb6983"
        #     print("requestUrl=",requestUrl)
        #     request = scrapy.Request(requestUrl, self.parseData)
        #     request.meta['longitude'] = longitudes[zuobiaoIndex]
        #     request.meta['latitude'] = latitudes[zuobiaoIndex]
        #     yield request
        longitudeFrom = 117.65
        longitudeTo = 118.00
        latitudeFrom = 39.13
        latitudeTo = 40.00

        longitudeSpace = 0.07
        longitudeSize = 12

        latitudeSpace = 0.045
        latitudeSize = 17
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
