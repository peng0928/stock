import re
import orjson
import json
import sys
import pymongo
import datetime

from dateutil.relativedelta import relativedelta
from loguru import logger as MonLog
from bson.objectid import ObjectId
from datetime import timedelta
from gridfs import GridFS
from pymongo.errors import DocumentTooLarge
from sshtunnel import SSHTunnelForwarder


class Log():

    def __init__(self, log=True):
        self.log = log

    def info(self, msg):
        if self.log:
            MonLog.info(msg)

    def warning(self, msg):
        if self.log:
            MonLog.warning(msg)

    def success(self, msg):
        if self.log:
            MonLog.success(msg)

    def error(self, msg):
        if self.log:
            MonLog.error(msg)

    def debug(self, msg):
        if self.log:
            MonLog.debug(msg)

    def exception(self, msg):
        if self.log:
            MonLog.exception(msg)





class MongoConn:
    def __init__(self, host='192.168.15.100', port=27017, db='MongoTest', log=True):
        self.myclient = pymongo.MongoClient('127.0.0.1', port=port)
        self.mydb = self.myclient[db]
        self.Mlog = Log(log=log)
        self.Mlog.success('Mongodb连接成功')

    @property
    def db(self):
        return self.mydb

    def col(self, collection):
        return self.mydb[collection]

    def exist_db(self, db):
        msg = '数据库:{} {}存在'
        dblist = self.myclient.list_database_names()
        if str(db) in dblist:
            self.Mlog.info(msg.format(db, ''))
            return True
        else:
            self.Mlog.info(msg.format(db, '不'))
            return False

    def exist_collection(self, collection):
        msg = '数据库:{} {}存在'
        collist = self.mydb.list_collection_names()
        if collection in collist:  # 判断 sites 集合是否存在
            self.Mlog.info(msg.format(collection, ''))
            return True
        else:
            self.Mlog.info(msg.format(collection, '不'))
            return False

    def create(self, collection):
        self.mydb[collection]
        self.Mlog.success(f'{collection} 集合创建成功')

    def insert(self, collection, mydict, expire_time=False):
        try:
            mycol = self.mydb[collection]
            result = mycol.insert_one(mydict)
            self.Mlog.success(
                f'数据插入成功 -> Data: {mydict} collection: {collection}')
            inserted_id = result.inserted_id

            if expire_time:
                mycol.create_index(
                    "created_at", expireAfterSeconds=0)  # 确保已经创建 TTL 索引
                mycol.update_one({"_id": inserted_id}, {
                    "$set": {"created_at": expire_time}})
            return inserted_id
        except Exception as e:
            print(e)
            return None

    def insert_many(self, collection, mylist):
        mycol = self.mydb[collection]
        result = mycol.insert_many(mylist)
        self.Mlog.success(f'数据插入成功 -> Data: {result} collection: {collection}')

    def find(self, collection):
        mycol = self.mydb[collection]
        result = mycol.find_one()
        self.Mlog.success(f'数据查询成功 -> Data: {result} collection: {collection}')
        return result

    def delete(self, collection, ids):
        query = {"_id": ObjectId(ids)}
        mycol = self.mydb[collection]
        mycol.delete_one(query)
        self.Mlog.success(f'数据删除成功 ->%s' % ids)
        return None

    def delete_query(self, collection, query):
        mycol = self.mydb[collection]
        mycol.delete_many(query)
        self.Mlog.success(f'数据删除成功 ->%s' % query)
        return None

    def findall(self, collection, condition: dict = {}, sortfield="time", limit: str or int = 10, sort=-1):
        result_list = []
        mycol = self.mydb[collection]
        result = mycol.find(condition)
        if sortfield:
            result = result.sort(sortfield, sort)
        if limit:
            result = result.limit(limit)
        for res in result:
            result_list.append(res)
        self.Mlog.success(
            f'数据查询成功 -> Data: {result_list} collection: {collection}')
        return result_list

    def find_id(self, collection, ids: str):
        mycol = self.mydb[collection]
        result = mycol.find({"_id": ObjectId(ids)})
        result = list(result)
        self.Mlog.success(f'数据查询成功 -> Data: {result} collection: {collection}')
        return result

    def create_index(self, collection, field: str):
        mycol = self.mydb[collection]
        result = mycol.create_index([("timestamp", pymongo.ASCENDING), "eliot"])
        self.Mlog.success(f'create_index -> Data: {result} collection: {collection}')
        return result

    def update_one(self, collection, filter, data, upsert=False):
        try:
            mycol = self.mydb[collection]
            query = {'$set': data}
            mycol.update_one(filter, query, upsert=upsert)
            self.Mlog.success(f'数据更新成功 -> filter: {filter} query: {query}')
            return True
        except Exception as e:
            print(e)
            return False

    def update_many(self, collection, filter, data):
        try:
            mycol = self.mydb[collection]
            query = {'$set': data}
            mycol.update_many(filter, query)
            self.Mlog.success(f'数据更新成功 -> filter: {filter} query: {query}')
            return True
        except Exception as e:
            print(e)
            return False

    def find_query(self, collection, find_query, sort_field=None, sort_order=None, log=False, limit: int = None):
        mycol = self.mydb[collection]
        if limit:
            result = mycol.find(find_query).limit(limit)
        else:
            result = mycol.find(find_query)
        result.sort(sort_field, sort_order) if sort_field else result
        result = list(result)
        if log:
            self.Mlog.success(
                f'数据查询成功 -> Data: {result} collection: {collection}')
        return result

    def count(self, collection, query):
        mycol = self.mydb[collection]
        count_documents = mycol.count_documents(query)
        # print(f"匹配查询条件的文档数量为: {count_documents}")
        return count_documents

    def find_state(self, collection, query):
        batch_size = 1000
        mycol = self.mydb[collection]
        cursor = mycol.find(query).batch_size(batch_size)
        return cursor

    def test(self, collection, query):
        mycol = self.mydb[collection]
        for index, document in enumerate(mycol.find(batch_size=1000)):
            print(index)


def months_precise(date_str1, date_str2, date_format="%Y-%m-%d"):
    date1 = datetime.datetime.strptime(date_str1, date_format)
    date2 = datetime.datetime.strptime(date_str2, date_format)

    # 使用relativedelta来计算更精确的月份差异
    delta = relativedelta(date2, date1)
    return delta.years * 12 + delta.months


if __name__ == '__main__':
    MonConn = MongoConn(log=True, db='KafkaPro')
    now = datetime.datetime.now()
    days_ago = str(now - datetime.timedelta(days=30))[:-7]
    days_ago_stamp = int(datetime.datetime.strptime(days_ago, "%Y-%m-%d %H:%M:%S").timestamp() * 1000)
    query = {
        "area": 'fujian',
        "topic": 'increment_finance_table_status_prod',
        'timestamp': {
            '$gte': days_ago_stamp,  # 大于等于7天前的时间戳
        }}
    json_list = MonConn.find_state('status_topic', query)
    print(json_list)
