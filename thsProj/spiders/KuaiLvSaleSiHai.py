import scrapy
import json
from ..items import DataItem
import time
import random
class newSpider(scrapy.Spider):
    name = "kuailvXiaoShouSiHai"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.KuaiLvSellCompanyInfoSiHai': 200
        }
    }

    def __init__(self,*args, **kwargs):
        pass

    start_urls = ["http://www.baidu.com"]

    # def parse(self, response):
        # requestUrl = "https://klcrm.meituan.com/crm/app/poi/r/list?pageNo=1&pageSize=20&cat1Id=&cat2Id=&customerLifecycleLabel=0&sortType=CREATETIME_DESC&onlineStatus=DEFAULT&ua=30402_ios&token=d7e567f07c*644b4896e6ec8c2bb6983"
        # request = scrapy.Request(requestUrl, self.parseData)
        # yield request

    def parse(self,response):
        # target_json = json.loads(response.body.decode("utf-8"))
        # print(target_json)
        # allPageSize = target_json['data']['page']['totalPageCount']
        for pageIndex in range(1,10):
            print(pageIndex)
            requestUrl = "https://klcrm.meituan.com/crm/app/poi/r/list?pageNo="+str(pageIndex)+"&pageSize=20&cat1Id=&cat2Id=&customerLifecycleLabel=0&sortType=CREATETIME_DESC&onlineStatus=DEFAULT&ua=30402_ios&token=d7e567f07c*644b4896e6ec8c2bb6983"
            request = scrapy.Request(requestUrl, self.saveData)
            time.sleep(random.randint(2,8))
            yield request
        time.sleep(20)


    def saveData(self,response):
        target_json = json.loads(response.body.decode("utf-8"))
        allCompany = target_json['data']['pageContent']
        print("-----------------pageSize = ",len(allCompany))
        for aCompany in allCompany:
            raw_item = DataItem()
            raw_item = aCompany
            yield raw_item
