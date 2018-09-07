import json
import MySQLdb
import time

# for i in range(1,39):
#     print(i)
MYSQL_CONFIG = {
    'host': '47.104.142.246',
    'user': 'root',
    'passwd': 'yanglu56',
    'port':3360,
    'db': 'ths',
    'charset': 'utf8'
}
conn = MySQLdb.connect(host="47.104.142.246",port=3360,user="root",passwd="yanglu56",db="ths",charset="utf8")
conn.autocommit(True)
cursor = conn.cursor()
cursor = conn.cursor()

tableName = "z_kuailv_company_detail_public"
publicFrom = "public"
toTable = "kuailv_company_detail"
cursor.execute("select max(id),min(id) from " + tableName)
maxMinId = cursor.fetchone()
maxId = maxMinId[0]
minId = maxMinId[1]
print(maxId," ", minId)
SPACE = 1000
for fromId in range(minId,maxId,SPACE):
    cursor.execute("select alldata from " + tableName + " where id >= " + str(fromId) + " and id < " + str(fromId + SPACE))
    allData = list(cursor.fetchall())
    print(fromId)
    for aData in allData:
        aContent = aData[0]
        tmpContent = str(aContent).replace('\'','"')
        tmpContent = tmpContent.replace(' ','')
        tmpContent = tmpContent.replace('False','"False"')
        tmpContent = tmpContent.replace('True','"True"')

        # newContent = "'" + newContent + "'"
        # print(newContent)
        item = json.loads(tmpContent,strict=False)
        # private 需要加入bdTel字段
        try:
            insertSql = 'insert into ' + toTable + '(wmBind,mapPoiName,latitude,onlineStatus,outOfRange,cityId,bdName,poiPositionTypeId,busArea,bdId,cityName,businessTypeName,countyId,street,guideDesc,houseNo,poiId,poiTag,cat1Name,closeReason,countyName,longitude,buId,address,poiName,operateType,cat1Id,cat2Id,provinceId,wmPoiId,businessTypeId,cat2Name,cooperated,businessPatternName,poiPositionTypeName,provinceName,businessPatternId,public) values("%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s","%s")'\
                        %(str(item["wmBind"]),str(item["mapPoiName"]),str(item["latitude"]),str(item["onlineStatus"]),str(item["outOfRange"]),str(item["cityId"]),str(item["bdName"]),str(item["poiPositionTypeId"]),str(item["busArea"]),str(item["bdId"]),str(item["cityName"]),str(item["businessTypeName"]),str(item["countyId"]),str(item["street"]),str(item["guideDesc"]),str(item["houseNo"]),str(item["poiId"]),str(item["poiTag"]),str(item["cat1Name"]),str(item["closeReason"]),str(item["countyName"]),str(item["longitude"]),str(item["buId"]),str(item["address"]),str(item["poiName"]),str(item["operateType"]),str(item["cat1Id"]),str(item["cat2Id"]),str(item["provinceId"]),str(item["wmPoiId"]),str(item["businessTypeId"]),str(item["cat2Name"]),str(item["cooperated"]),str(item["businessPatternName"]),str(item["poiPositionTypeName"]),str(item["provinceName"]),str(item["businessPatternId"]),publicFrom)
            cursor.execute(insertSql)
        except Exception as err:
            print(item)
            print(err)


conn.close()


