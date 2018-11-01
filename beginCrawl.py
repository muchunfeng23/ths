from scrapy import cmdline
import os
import time,datetime
# os.system("scrapy crawl 1_day_lhb")
# os.system("scrapy crawl 1_day_share_info_everyday")
# os.system("scrapy crawl 1_day_stastic_big_num")


# week_day_dict = {
#         0: '星期一',
#         1: '星期二',
#         2: '星期三',
#         3: '星期四',
#         4: '星期五',
#         5: '星期六',
#         6: '星期天',
#     }
# day = datetime.datetime.now().weekday()
# print("day=",week_day_dict[day])
# if day == 5 or day == 6:
#     pass
# else:
#     os.system("scrapy crawl 1_day_lhb")
#     os.system("scrapy crawl 1_day_dfcf_hq")


os.system("scrapy crawl 1_day_lhb")
os.system("scrapy crawl 1_day_dfcf_hq")
os.system("scrapy crawl big_orders")








    # 下面方法获取数据过多，先暂且不用
    # os.system("scrapy crawl 1_day_stastic_big_num")
    # 下面的方法目前只适合在windows下运行
    # os.system("scrapy crawl 1_day_share_info_everyday_use_click")


# os.system("scrapy crawl kuailvCompanyOrderList")
# os.system("scrapy crawl kuailvXiaoShou")



# cmdline.execute("scrapy crawl 1_day_lhb".split())
# cmdline.execute("scrapy crawl 1_day_share_info_everyday_use_click".split())





# cmdline.execute("scrapy crawl 1_day_stastic_big_num".split())


# 一礼拜一次,板块信息
# cmdline.execute("scrapy crawl 1_week_share_plate_spider".split())





