from PrSpider import Xpath
import requests

from loguru import logger
from utils.tools.index import to_yi
from functools import wraps


def catch_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            print(e)
            logger.warning(f"catch_exceptions => {e}")
            raise e
            return {"status": False, "msg": "服务暂不可用"}

    return wrapper


class RequestClient:

    def __init__(self, **kwargs):
        self.headers = {
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36",
        }
        self.headers_form = {
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
            'Host': 'kyfw.12306.cn',
            'Origin': 'https://kyfw.12306.cn',
            'Referer': 'https://kyfw.12306.cn/otn/passport?redirect=/otn/login/userLogin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0.0.0 Safari/537.36',
        }
        self.cookie = kwargs.get('cookie')
        self.session = requests.session()
        self.session.headers = self.headers

    @catch_exceptions
    def stock_get(self, code):
        main_url = f"https://data.eastmoney.com/stockdata/{code}.html"
        response = self.session.get(main_url)
        tree = Xpath(response.text)
        code = tree.xpath("//li[@id='stock_name1']/@data").get()
        hy = tree.xpath("//ul[@id='tab_list1']/li[@id='bk1']/@data").get()
        dp = tree.xpath("//ul[@id='tab_list1']/li[@id='dp1']/@data").get()
        url = "https://push2.eastmoney.com/api/qt/stock/get"
        params = {
            "fltt": "2",
            "invt": "2",
            "secid": code,
            "fields": "f57,f58,f107,f43,f169,f170,f171,f47,f48,f60,f46,f44,f45,f168,f50,f162,f177,f117,f167,f116,f168",
            "ut": "",
            "cb": "",
            "_": ""
        }
        response = self.session.get(url, params=params)
        json_data = response.json()
        print(json_data)
        json_data = json_data.get('data') or {}
        item = {
            "cha": json_data.get('f169'),  # 涨跌额
            "chg": json_data.get('f170'),  # 涨跌幅
            "end": json_data.get('f43'),  # 今收
            "now": json_data.get('f46'),  # 今开
            "max": json_data.get('f44'),  # 最高
            "min": json_data.get('f45'),  # 最低
            "turnover": to_yi(json_data.get('f47')),  # 成交量
            "market": to_yi(json_data.get('f116')),  # 总市值
            "float_market": to_yi(json_data.get('f117')),  # 流通市值
            "P_E": json_data.get('f162'),  # 市盈
            "market_net": json_data.get('f167'),  # 市净
            "code": json_data.get('f57'),  # 股票代码
            "name": json_data.get('f58'),  # 股票名称
            "hy": hy,
            "dp": dp,
            "cid": code,
        }
        return item

    @catch_exceptions
    def stock_trends(self, code):
        url = "https://push2.eastmoney.com/api/qt/stock/trends2/get"
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
            "ut": "",
            "iscr": "0",
            "ndays": "1",
            "secid": code,
            "cb": "",
            "_": ""
        }
        response = self.session.get(url, params=params)
        json_data = response.json()
        json_data = json_data.get('data') or {}
        prePrice = json_data.get('prePrice') or {}
        trends = json_data.get('trends') or {}
        trend_item = []
        if trends:
            oepn = trends[0].split(',')[1]
            end = trends[-1].split(',')[2]
            result = round(round(float(float(end) - prePrice) / float(prePrice), 4) * 100, 2)
            for i in trends:
                trend_data = i.split(',')
                increase = round(float(trend_data[2]) - float(prePrice), 2)
                ratio = round((increase / float(prePrice) * 100), 2)
                trend_dict = {
                    "open_price": trend_data[1],  # k线开盘价
                    "price": trend_data[2],  # k线当前价
                    "max_price": trend_data[3],  # k线最高价
                    "min_price": trend_data[4],  # k线最低价
                    "cjl": trend_data[5],  # 成交量
                    "cje": trend_data[6],  # 成交额
                    "ratio": f"{ratio}%",
                    "increase": increase,
                    "datetime": trend_data[0][-5:],  # 时间
                    "show": "1"
                }
                trend_item.append(trend_dict)
        else:
            oepn = '-'
            end = '-'
            result = '-'
        item = {
            "name": json_data.get('name'),  # 股票名称
            "code": json_data.get('code'),  # 股票代码
            "oepn": oepn,  # 开盘价
            "end": end,  # 收盘价
            "rate": result,  # 比例
            "trends": trend_item,  # 信息
        }
        return item

    @catch_exceptions
    def stock_trends2(self, code):
        url = "https://push2.eastmoney.com/api/qt/stock/trends2/get"
        params = {
            "fields1": "f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13",
            "fields2": "f51,f52,f53,f54,f55,f56,f57,f58",
            "ut": "",
            "iscr": "0",
            "ndays": "1",
            "secid": code,
            "cb": "",
            "_": ""
        }
        response = self.session.get(url, params=params)
        json_data = response.json()
        json_data = json_data.get('data') or {}
        prePrice = json_data.get('prePrice') or {}
        trends = json_data.get('trends') or {}
        name = json_data.get('name')
        if trends:
            oepn = trends[0].split(',')[1]
            end = trends[-1].split(',')[2]
            result = round(round(float(float(end) - prePrice) / float(prePrice), 4) * 100, 2)
        else:
            oepn = '-'
            end = '-'
            result = '-'
        item = {
            "name": name,  # 股票名称
            "code": json_data.get('code'),  # 股票代码
            "oepn": oepn,  # 开盘价
            "end": end,  # 收盘价
            "rate": result,  # 比例
            # "trends": trends,  # 信息
        }
        if not name:
            return {}
        return item

    @catch_exceptions
    def stock_securities(self, code):
        item = []
        url = "https://datacenter-web.eastmoney.com/api/data/v1/get"
        params = {
            "callback": "",
            "reportName": "RPT_F10_ORG_BASICINFO",
            "columns": "ALL",
            "sortColumns": "",
            "sortTypes": "",
            "source": "WEB",
            "client": "WEB",
            "filter": f"(SECURITY_CODE=\"{code}\")",
            "_": ""
        }
        response = self.session.get(url, params=params)
        code = response.json().get('result').get('data')[0].get('SECUCODE')
        url = "https://datacenter.eastmoney.com/securities/api/data/v1/get"
        params = {
            "reportName": "RPT_F10_RELATE_GN",
            "columns": "SECUCODE,SECURITY_CODE,SECURITY_NAME_ABBR,ORG_CODE,BOARD_CODE,BOARD_NAME,BOARD_TYPE_NEW",
            "quoteColumns": "",
            "filter": f"(SECUCODE=\"{code}\")(BOARD_TYPE_NEW=\"3\")",
            "pageNumber": "1",
            "pageSize": "",
            "sortTypes": "",
            "sortColumns": "",
            "source": "HSF10",
            "client": "PC",
            "v": ""
        }
        response = self.session.get(url, params=params)
        json_data = response.json().get('result').get('data')
        for key in json_data:
            name = key.get('BOARD_NAME')
            url = f"https://searchadapter.eastmoney.com/api/suggest/get?input={name}&type=14&token=&markettype=&mktnum=&jys=&classify=&securitytype=&status=&count=&_="
            response = self.session.get(url, params=params)
            data = response.json().get('QuotationCodeTable').get('Data')[0]
            bid = data.get("QuoteID")
            item_data = self.stock_trends2(bid)
            item.append(item_data)
        return item


def main():
    client = RequestClient()
    stock_data = client.stock_get('002045')
    print(stock_data)


if __name__ == '__main__':
    main()
