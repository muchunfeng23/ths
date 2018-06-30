import scrapy
from ..items import ThsprojItem

class LHB_spider(scrapy.Spider):
    # 同花顺龙虎榜
    # 获取龙虎榜中买入卖出的营业厅
    # 使用数据方法：
    #       1、连续多日入榜单的
    #       2、结合股票板块信息，分析出每日进入龙虎榜最多的板块
    #       3、分析最近几天最活跃的板块

    name = "1_day_lhb"

    custom_settings = {
        'DOWNLOAD_DELAY': 1,
        'COOKIES_DEBUG': True,
        'RANDOMIZE_DOWNLOAD_DELAY': True,
        'ITEM_PIPELINES': {
            'thsProj.pipelines.ThsprojPipeline': 200
        }
    }

    def __init__(self):
        pass

    start_urls = ["http://data.10jqka.com.cn/market/longhu/"]

    def parse(self, response):
        bigPeopleInfos = response.xpath('//*[@id="ggmx"]/div[2]/div[3]/div[2]')[0]
        allStocks = bigPeopleInfos.xpath('./div')
        for oneStock in allStocks[0:len(allStocks) - 1]:
            # reason
            try:
                onListReason = oneStock.xpath('./p/text()').extract()[0]
                indexPre = onListReason.index("(")
                indeEnd = onListReason.index(")")
                shareCode = onListReason[indexPre+1:indeEnd]
                buyPeoples = oneStock.xpath('./div[2]/table[1]/tbody/tr')
                sellPeoples = oneStock.xpath('./div[2]/table[2]/tbody/tr')
                for trs1 in buyPeoples:
                    item = ThsprojItem()
                    bigData = {}
                    bigPeopleName = trs1.xpath('./td[1]/a/text()').extract()[0]
                    orgCodeLink = trs1.xpath('./td[1]/a').extract()[0]
                    if orgCodeLink.find("jgzy") > 0:
                        orgCode = "jgzy"
                    else:
                        orgCodePreIndex = orgCodeLink.index('orgcode/')+len('orgcode/')
                        orgCodeEndIndex = orgCodeLink.index("target") - 3
                        orgCode = orgCodeLink[orgCodePreIndex:orgCodeEndIndex]
                    buy_in = trs1.xpath('./td[2]/text()').extract()[0]
                    sell_out = trs1.xpath('./td[3]/text()').extract()[0]
                    amount = trs1.xpath('./td[4]/text()').extract()[0]
                    bigData["share_code"] = shareCode
                    bigData["on_list_reason"] = onListReason
                    bigData["org_code"] = orgCode
                    bigData["big_people"] = bigPeopleName
                    bigData["buy_in"] = buy_in
                    bigData["sell_out"] = sell_out
                    bigData["amount"] = amount
                    item = bigData
                    yield item

                for trs2 in sellPeoples:
                    item2 = ThsprojItem()
                    bigData2 = {}
                    bigPeopleName2 = trs2.xpath('./td[1]/a/text()').extract()[0]
                    orgCodeLink2 = trs2.xpath('./td[1]/a').extract()[0]
                    if orgCodeLink2.find("jgzy") > 0:
                        orgCode2 = "jgzy"
                    else:
                        orgCodePreIndex2 = orgCodeLink2.index('orgcode/') + len('orgcode/')
                        orgCodeEndIndex2 = orgCodeLink2.index("target") - 3
                        orgCode2 = orgCodeLink2[orgCodePreIndex2:orgCodeEndIndex2]
                    buy_in2 = trs2.xpath('./td[2]/text()').extract()[0]
                    sell_out2 = trs2.xpath('./td[3]/text()').extract()[0]
                    amount2 = trs2.xpath('./td[4]/text()').extract()[0]
                    bigData2["share_code"] = shareCode
                    bigData2["on_list_reason"] = onListReason
                    bigData2["org_code"] = orgCode2
                    bigData2["big_people"] = bigPeopleName2
                    bigData2["buy_in"] = buy_in2
                    bigData2["sell_out"] = sell_out2
                    bigData2["amount"] = amount2
                    item2 = bigData2
                    yield item2
            except Exception as err:
                print(err)
                # print(oneStock)
        pass



