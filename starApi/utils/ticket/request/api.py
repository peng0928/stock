import datetime
import json

from PrSpider import Xpath
import requests

from loguru import logger
from utils.tools.index import to_yi, to_float_list, merge_md
from functools import wraps


def catch_exceptions(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logger.exception(f"catch_exceptions => {e}")
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
        fields = ['f58', 'f734', 'f107', 'f57', 'f43', 'f59', 'f169', 'f301', 'f60', 'f170', 'f152', 'f177', 'f111',
                  'f46', 'f44', 'f45', 'f47', 'f260', 'f48', 'f261', 'f279', 'f277', 'f278', 'f288', 'f19', 'f17',
                  'f531', 'f15', 'f13', 'f11', 'f20', 'f18', 'f16', 'f14', 'f12', 'f39', 'f37', 'f35', 'f33', 'f31',
                  'f40', 'f38', 'f36', 'f34', 'f32', 'f211', 'f212', 'f213', 'f214', 'f215', 'f210', 'f209', 'f208',
                  'f207', 'f206', 'f161', 'f49', 'f171', 'f50', 'f86', 'f84', 'f85', 'f168', 'f108', 'f116', 'f167',
                  'f164', 'f162', 'f163', 'f92', 'f71', 'f117', 'f292', 'f51', 'f52', 'f191', 'f192', 'f262', 'f294',
                  'f295', 'f269', 'f270', 'f256', 'f257', 'f285', 'f286', 'f748', 'f747']

        fields = ','.join(fields)
        params = {
            "fltt": "2",
            "invt": "2",
            "secid": code,
            "fields": fields,
            "ut": "",
            "cb": "",
            "_": ""
        }
        response = self.session.get(url, params=params)
        json_data = response.json()
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
            "hs": f"{json_data.get('f168')}%",  # 换手
            "lb": json_data.get('f50'),  # 量比
            "zs": to_yi(json_data.get('f47')),  # 总手
            "je": to_yi(json_data.get('f48')),  # 金额
            "wp": to_yi(json_data.get('f49')),  # 外盘
            "np": to_yi(json_data.get('f161')),  # 内盘
            "zt": json_data.get('f51'),  # 涨停
            "dt": json_data.get('f52'),  # 跌停
            "zuos": json_data.get('f60'),  # 昨收
            "jk": json_data.get('f71'),  # 今开
            "zx": json_data.get('f43'),  # 最新
            "zf": json_data.get('f170'),  # 涨幅
            "jj": json_data.get('f71'),  # 均价
            "zd": "",  # 涨跌
            "hy": hy,
            "dp": dp,
            "cid": code,
            "md": '',
        }
        try:
            zd = round(float(json_data.get('f43')) - float(json_data.get('f71')), 2)
        except:
            zd = '-'
        item['zd'] = zd
        md_jg = [json_data.get('f32'), json_data.get('f34'), json_data.get('f36'),
                 json_data.get('f38'), json_data.get('f40'), json_data.get('f20'),
                 json_data.get('f18'), json_data.get('f16'), json_data.get('f14'), json_data.get('f12'),
                 ]
        try:
            md = merge_md(to_float_list(json_data.get('f43'), json_data.get('f51')), md_jg)
            item['md'] = md
        except:
            item['md'] = ''
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
                    "jj": trend_data[7],  # 均价
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

    @catch_exceptions
    def stock_details(self, code):
        url = "https://push2.eastmoney.com/api/qt/stock/details/get"
        params = {
            "fields1": "f1,f2,f3,f4",
            "fields2": "f51,f52,f53,f54,f55^",
            "fltt": "2",
            "cb": "",
            "pos": "",
            "secid": code,
            "ut": "",
            "wbp2u": "|0|0|0|web",
            "_": "^"
        }
        response = self.session.get(url, params=params)
        json_data = response.json().get('data').get('details')
        if json_data:
            json_data = [i.split(',') for i in json_data]
        return json_data

    @catch_exceptions
    def stock_zs(self):
        """
        获取上证、深圳指数信息
        :return:
        """
        url = f"https://push2.eastmoney.com/api/qt/ulist.np/get"
        params = {
            "cb": "",
            "fltt": "2",
            "secids": "1.000001,0.399001",
            "fields": "f1,f2,f3,f4,f6,f12,f13,f104,f105,f106",
            "ut": "",
            "_": ""
        }
        response = self.session.get(url, params=params)
        json_data = response.json()
        json_data = json_data.get('data').get('diff') or {}
        item = {
            "shz": json_data[0].get('f2'),
            "sz": json_data[1].get('f2'),
        }
        return json.dumps(item)

    @catch_exceptions
    def stock_bk(self):
        """
        获取板块信息
        :return:
        """
        item = []
        url = "https://push2.eastmoney.com/api/qt/clist/get"
        params = {
            "cb": "",
            "fid": "f62",
            "po": "1",
            "pz": "1000",
            "pn": "1",
            "np": "1",
            "fltt": "2",
            "invt": "2",
            "ut": "",
            "fs": "m:90 t:2",
            "fields": "f12,f14,f2,f3,f62,f184,f66,f69,f72,f75,f78,f81,f84,f87,f204,f205,f124,f1,f13"
        }
        response = self.session.get(url, params=params)
        json_data = response.json()
        json_data = json_data.get('data').get('diff') or {}
        for val in json_data:
            item.append({
                "name": val.get('f14'),
                "zdg": val.get('f204'),
                "zf": val.get('f3'),
                "zlje": to_yi(val.get('f62')),
                "zljzb": val.get('f184'),
                "jrcddje": to_yi(val.get('f66')),
                "jrcddjzb": val.get('f69'),
                "jrddje": to_yi(val.get('f72')),
                "jrddjzb": val.get('f75'),
                "jrzdje": to_yi(val.get('f78')),
                "jrzdjzb": val.get('f81'),
                "jrxdje": to_yi(val.get('f84')),
                "jrxdjzb": val.get('f87'),
            })
        return item

    @catch_exceptions
    def stock_ZTPool(self):
        """
        获取涨停板信息
        :return:
        """
        item = []
        url = "https://push2ex.eastmoney.com/getTopicZTPool"
        date = datetime.datetime.now().strftime("%Y%m%d")
        params = {
            "cb": "",
            "ut": "7eea3edcaed734bea9cbfc24409ed989",
            "dpt": "wz.ztzt",
            "Pageindex": "0",
            "pagesize": "1000",
            "sort": "fbt:asc",
            "date": date,
            "_": ""
        }
        response = self.session.get(url, params=params)
        json_data = response.json()
        json_data = json_data.get('data').get('pool') or {}
        if json_data:
            for index, val in enumerate(json_data):
                item.append({
                    "code": val.get('c'),
                    "name": val.get('n'),
                    "zd": val.get('zdp'),
                    "zxj": val.get('p'),
                    "cje": val.get('amount'),
                    "zsz": val.get('tshare'),
                    "hs": val.get('hs'),
                    "fbjj": val.get('fund'),
                    "ltsz": val.get('ltsz'),
                    "fbt": val.get('fbt'),
                    "lbt": val.get('lbt'),
                    "zbcs": val.get('zbc'),
                    "lbs": val.get('lbc'),
                    "hy": val.get('hybk'),
                    "zttj": val.get('zttj'),
                    "inx": str(index + 1),
                })
        return item


def main():
    client = RequestClient()
    # stock_data = client.stock_details('0.002131')
    stock_data = client.stock_ZTPool()
    print(stock_data)


if __name__ == '__main__':
    main()
