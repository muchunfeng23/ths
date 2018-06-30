# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import MySQLdb
from scrapy.conf import settings
from .commvars import StrDate
import time

now = StrDate.now()
nowdate = now.datekey

class ThsprojPipeline(object):
    # Initialize database environment.
    def open_spider(self, spider):
        self.conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute('insert into crawler_lhb_big_people (share_code,on_list_reason,org_code,big_people,buy_in,sell_out,amount,c_t,datekey) values("%s","%s","%s","%s","%s","%s","%s","%d","%d")'
                            %(item["share_code"],item["on_list_reason"],item["org_code"],item["big_people"],item["buy_in"],item["sell_out"],item["amount"],int(time.time()),int(nowdate)))



class ShareDataEveryDay(object):
    # Initialize database environment.
    def open_spider(self, spider):
        self.conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute('insert into crawler_share_everyday_data (share_code,share_name,now_price,rise_fall_ratio,rise_fall,rise_speed,quantity_ratio,exchange_radio,amplitude,turnover,circulation_stock_desc,circulation_stock,circulation_value_desc,circulation_value,pe_ration,c_t,datekey) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%d")'
                            %(item["share_code"],item["share_name"],item["now_price"],item["rise_fall_ratio"],item["rise_fall"],item["rise_speed"],item["quantity_ratio"],item["exchange_radio"],item["amplitude"],item["turnover"],item["circulation_stock_desc"],item["circulation_stock"],item["circulation_value_desc"],item["circulation_value"],item["pe_ration"],int(time.time()),int(nowdate)))
        pass


class SharePlateData(object):
    # Initialize database environment.
    def open_spider(self, spider):
        self.conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute('insert into crawler_share_plate_info (share_code,plate_name,desc1,c_t,datekey) values("%s","%s","%s","%d","%d")'
                            %(item["share_code"],item["plate_name"],str(item["desc"]),int(time.time()),int(nowdate)))
        pass
