import scrapy
from ..items import DataItem
from scrapy.conf import settings
import MySQLdb

class SharePlateInfo(scrapy.Spider):
    name = "1_week_share_plate_spider"
    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.SharePlateData': 200
        }
    }

    def __init__(self,*args, **kwargs):
        self.readAllShares()
        pass

    start_urls = ["http://www.baidu.com"]

    def parse(self, response):
        for shareCodeNum in range(len(self.allShares)):
            shareCode = self.allShares[shareCodeNum][0]
            request2 = scrapy.Request("http://basic.10jqka.com.cn/"+shareCode+"/concept.html",callback=self.parsePlate)
            request2.meta["shareCode"] = shareCode
            yield request2

    def parsePlate(self,response):
        allPlates = response.xpath('//*[@id="concept"]/div[2]/div/table/tbody/tr')
        for i in range(0, len(allPlates), 2):
            aTr = allPlates[i]
            aTrDesc = allPlates[i + 1]
            item = DataItem()
            plate = {}

            plate["share_code"] = response.meta["shareCode"]
            platNameInfo = aTr.xpath('./td[2]/text()').extract()[0]
            if platNameInfo.find("<a") > 0:
                indexOfA = platNameInfo.index("<a")
                tmpInfo = platNameInfo[0:indexOfA]
                realInfo = tmpInfo.replace('"', '').replace("\n", "").replace("\t", "").replace(" ", "").replace("\xa0","").replace("\\","")
                plate["plate_name"] = realInfo
            else:
                plate["plate_name"] = platNameInfo.replace('"', '').replace("\n", "").replace("\t", "").replace(" ", "").replace("\xa0","").replace("\\","")
            try:
                desc = aTrDesc.xpath('./td/div/text()').extract()[1].replace("\n", "").replace("\t", "").replace(" ", "").replace("\xa0","").replace("\\","").replace("\"","'")
                plate["desc"] = desc
            except Exception:
                plate["desc"] = ""
                pass
            item = plate
            yield item

    def readAllShares(self):
        conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        cursor = conn.cursor()
        cursor.execute("select share_code from all_shares")
        self.allShares = list(cursor.fetchall())
        print(self.allShares)