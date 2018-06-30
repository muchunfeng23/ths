import scrapy
from ..items import DataItem

class PlatInfo(scrapy.Spider):
    name = "test"
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.SharePlateData': 200
        }
    }
    def __init__(self):
        pass

    start_urls = ["http://basic.10jqka.com.cn/002494/concept.html"]

    def parse(self, response):
        allPlates = response.xpath('//*[@id="concept"]/div[2]/div/table/tbody/tr')
        # //*[@id="concept"]/div[2]/div/table/tbody/tr[1]/td[2]
        for i in range(0, len(allPlates), 2):
            aTr = allPlates[i]
            aTrDesc = allPlates[i + 1]
            item = DataItem()
            plate = {}

            plate["share_code"] = 1
            platNameInfo = aTr.xpath('./td[2]/text()').extract()[0]
            if platNameInfo.find("<a") > 0:
                indexOfA = platNameInfo.index("<a")
                tmpInfo = platNameInfo[0:indexOfA]
                realInfo = tmpInfo.replace('"', '').replace("\n", "")\
                    .replace("\t", "").replace(" ", "").replace("\xa0","").replace("\\", "")
                plate["plate_name"] = realInfo
            else:
                plate["plate_name"] = platNameInfo.replace('"', '').replace("\n", "").replace("\t", "").replace(" ","").replace("\xa0", "").replace("\\", "")
            desc = aTrDesc.xpath('./td/div/text()').extract()[1].replace("\n", "").replace("\t", "").replace(" ","").replace("\xa0", "").replace("\\", "")
            print("-----------", desc)
            plate["desc"] = desc
            item = plate
            yield item
