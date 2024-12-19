import time

from utils.client.mongoApi import MongoConn
from utils.ticket.request.api import RequestClient
from utils.ticket.request.tool.ticket_tool import *
from concurrent.futures import ThreadPoolExecutor

Executor = ThreadPoolExecutor(max_workers=10)
Request = RequestClient()
MongoClient = MongoConn(db='Stock')


class Stock:

    def kline(self):
        while True:
            date_now = get_datetime()
            get_mongo = MongoClient.find_query('stock_kline', find_query={"date": date_now})
            if get_mongo:
                print("[kline] 已存在")
                time.sleep(3600)
            else:
                shz_data = Request.stock_kline('1.000001')
                sz_data = Request.stock_kline('0.399001')
                save_item = {"date": date_now, "shz": shz_data, "sz": sz_data}
                MongoClient.insert('stock_kline', save_item)

    def duanban(self):
        while True:
            date_now = get_datetime()
            get_mongo = MongoClient.find_query('stock_duanban', find_query={"date": date_now})
            if get_mongo:
                print("[duanban] 已存在")
                time.sleep(3600)
            else:
                print("[duanban] 正在获取")
                data = Request.stock_dbcx()
                print("[duanban] 获取完成")
                save_item = {"date": date_now, "data":data}
                MongoClient.insert('stock_duanban', save_item)

def taskSchedule():
    stock = Stock()
    taskList = [stock.kline, stock.duanban]
    for task in taskList:
        Executor.submit(task)


if __name__ == '__main__':
    taskSchedule()
