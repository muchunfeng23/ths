# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES settingSharePlateData
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

    # def process_item(self, item, spider):
    #     self.cursor.execute('insert into crawler_share_everyday_data (share_code,share_name,now_price,rise_fall_ratio,rise_fall,rise_speed,quantity_ratio,exchange_radio,amplitude,turnover,circulation_stock_desc,circulation_stock,circulation_value_desc,circulation_value,pe_ration,c_t,datekey,index1) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%d","%d")'
    #                         %(item["share_code"],item["share_name"],item["now_price"],item["rise_fall_ratio"],item["rise_fall"],item["rise_speed"],item["quantity_ratio"],item["exchange_radio"],item["amplitude"],item["turnover"],item["circulation_stock_desc"],item["circulation_stock"],item["circulation_value_desc"],item["circulation_value"],item["pe_ration"],int(time.time()),int(nowdate),item["newIndex"]))
    #     pass

    def process_item(self, item, spider):
        self.cursor.execute(
            'insert into crawler_share_everyday_data (share_code,share_name,now_price,rise_fall_ratio,rise_fall,quantity_ratio,exchange_radio,amplitude,turnover,pe_ration,c_t,datekey,index1) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%d","%d","%d")'
            % (item["share_code"], item["share_name"], item["now_price"], item["rise_fall_ratio"], item["rise_fall"],
               item["quantity_ratio"], item["exchange_radio"], item["amplitude"], item["turnover"],item["pe_ration"], int(time.time()), int(nowdate), item["newIndex"]))
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





class KuaiLvSellCompanyInfo(object):
    def open_spider(self, spider):
        self.conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute('insert into z_kuailv_seller_company_info (poiId,poiName,cityId,cityName,countryId,countryName,street,houseNo,busArea,onlineStatus,cat1Id,cat2Id,cat1Name,cat2Name,wmPoiId,wmBind,poiTag,lifecycleLabelId,lifecycleLabelName,businessTypeId,businessPatternId,businessStartTime,businessEndTime,poiPositionTypeId,addrAbnormal,closeReason,mapPoiName,address,wmPoiInfo,bdId,bdName,belongStatus,operateType,distance,customerLifecycleLabel,customerLifecycleLabelName) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                            %(str(item["poiId"]),str(item["poiName"]),str(item["cityId"]),str(item["cityName"]),str(item["countyId"]),str(item["countyName"]),str(item["street"]),str(item["houseNo"]),str(item["busArea"]),str(item["onlineStatus"]),str(item["cat1Id"]),str(item["cat2Id"]),str(item["cat1Name"]),str(item["cat2Name"]),str(item["wmPoiId"]),str(item["wmBind"]),str(item["poiTag"]),str(item["lifecycleLabelId"]),str(item["lifecycleLabelName"]),str(item["businessTypeId"]),str(item["businessPatternId"]),str(item["businessStartTime"]),str(item["businessEndTime"]),str(item["poiPositionTypeId"]),str(item["addrAbnormal"]),str(item["closeReason"]),str(item["mapPoiName"]),str(item["address"]),str(item["wmPoiInfo"]),str(item["bdId"]),str(item["bdName"]),str(item["belongStatus"]),str(item["operateType"]),str(item["distance"]),str(item["customerLifecycleLabel"]),str(item["customerLifecycleLabelName"])))
        pass


class KuaiLvSellCompanyInfoSiHai(object):
    def open_spider(self, spider):
        self.conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute('insert into z_kuailv_seller_company_info_sihai (poiId,poiName,cityId,cityName,countyId,countyName,street,houseNo,busArea,onlineStatus,cat1Id,cat2Id,cat1Name,cat2Name,wmPoiId,wmBind,poiTag,lifecycleLabelId,lifecycleLabelName,businessTypeId,businessPatternId,businessStartTime,businessEndTime,poiPositionTypeId,addrAbnormal,closeReason,mapPoiName,address,wmPoiInfo,daysNoVisit,distance,kpName,kpTel,customerLifecycleLabel,customerLifecycleLabelName,kpId,couponLabel) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'
                            %(str(item["poiId"]),str(item["poiName"]),str(item["cityId"]),str(item["cityName"]),str(item["countyId"]),str(item["countyName"]),str(item["street"]),str(item["houseNo"]),str(item["busArea"]),str(item["onlineStatus"]),str(item["cat1Id"]),str(item["cat2Id"]),str(item["cat1Name"]),str(item["cat2Name"]),str(item["wmPoiId"]),str(item["wmBind"]),str(item["poiTag"]),str(item["lifecycleLabelId"]),str(item["lifecycleLabelName"]),str(item["businessTypeId"]),str(item["businessPatternId"]),str(item["businessStartTime"]),str(item["businessEndTime"]),str(item["poiPositionTypeId"]),str(item["addrAbnormal"]),str(item["closeReason"]),str(item["mapPoiName"]),str(item["address"]),str(item["wmPoiInfo"]),str(item["daysNoVisit"]),str(item["distance"]),str(item["kpName"]),str(item["kpTel"]),str(item["customerLifecycleLabel"]),str(item["customerLifecycleLabelName"]),str(item["kpId"]),str(item["couponLabel"])))
        pass



class KuaiLvKpidTelephone(object):
    def open_spider(self, spider):
        self.conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute('insert into z_kuailv_kpid_telephone (kpid,telephone) values("%s","%s")'
                            %(str(item["kpid"]),str(item["telephone"])))
        pass

class KuaiLvCompanyDetail(object):
    def open_spider(self, spider):
        self.conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute('insert into z_kuailv_company_detail (poiId,latitude,longitude,alldata) values("%s","%s","%s","%s")'
                            %(str(item["poiId"]),str(item["latitude"]),str(item["longitude"]),str(item["alldata"])))
        pass


class KuaiLvCompanyOrderList(object):
    def open_spider(self, spider):
        self.conn = MySQLdb.connect(**settings.get("MYSQL_CONFIG"))
        self.conn.autocommit(True)
        self.cursor = self.conn.cursor()

    def close_spider(self, spider):
        self.conn.close()

    def process_item(self, item, spider):
        self.cursor.execute('insert into z_kuailv_company_order_detail (poiId,orderid,alldata,ctime) values("%s","%s","%s","%s")'
                            %(str(item["poiId"]),str(item["orderid"]),str(item["alldata"]),str(item["ctime"])))
        pass
