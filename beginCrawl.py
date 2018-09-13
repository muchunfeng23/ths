from scrapy import cmdline
import os
import time,datetime
# os.system("scrapy crawl 1_day_lhb")
# os.system("scrapy crawl 1_day_share_info_everyday")
# os.system("scrapy crawl 1_day_stastic_big_num")


def get_week_day(date):
    week_day_dict = {
        0: '星期一',
        1: '星期二',
        2: '星期三',
        3: '星期四',
        4: '星期五',
        5: '星期六',
        6: '星期天',
    }
    day = date.weekday()
    return week_day_dict[day]
#
# date = datetime.datetime.now()
# if date.weekday == 5 or date.weekday == 6:
#     pass
# else:
#     os.system("scrapy crawl 1_day_lhb")
#     # 下面方法获取数据过多，先暂且不用
#     # os.system("scrapy crawl 1_day_stastic_big_num")
#     # 下面的方法目前只适合在windows下运行
#     # os.system("scrapy crawl 1_day_share_info_everyday_use_click")


# os.system("scrapy crawl kuailvCompanyOrderList")
# os.system("scrapy crawl kuailvXiaoShou")



# cmdline.execute("scrapy crawl 1_day_lhb".split())
# cmdline.execute("scrapy crawl 1_day_share_info_everyday_use_click".split())




os.system("scrapy crawl 1_day_lhb")
os.system("scrapy crawl 1_day_dfcf_hq")
# cmdline.execute("scrapy crawl 1_day_stastic_big_num".split())


# 一礼拜一次,板块信息
# cmdline.execute("scrapy crawl 1_week_share_plate_spider".split())





