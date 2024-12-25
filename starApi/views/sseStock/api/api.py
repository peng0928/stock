import time
import json
import hashlib
import asyncio
import aiohttp

from fastapi import *
from fastapi.routing import APIRouter
from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.responses import StreamingResponse
from loguru import logger
from utils.tools.index import jsons, to_yi
from utils.ticket.request.api import *

ReqClient = RequestClient()

router = APIRouter(
    prefix="/api",
    tags=["test"],
    default_response_class=ORJSONResponse
)
# 存储从SSE接收到的数据


class SseData:
    info = {}
    detail = {}
    kline = []


current_sse_url = None
defaule_name = ['sse']
session = None
sse_time = 0.03
media_type = "text/event-stream"


def handle_sse(json_data, name=''):
    if name == 'sse_info':
        if json_data:
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
                # "hy": hy,
                # "dp": dp,
                # "cid": code,
                "md": '',
            }
            try:
                zd = round(float(json_data.get('f43')) -
                           float(json_data.get('f71')), 2)
            except:
                zd = '-'
            item['zd'] = zd
            SseData.info.update(item)
    elif name == 'kline':
        if json_data:
            trends = json_data.get('trends') or []
            prePrice = json_data.get('prePrice') or 0
            trend_item = []
            if trends:
                oepn = trends[0].split(',')[1]
                end = trends[-1].split(',')[2]
                result = round(
                    round(float(float(end) - prePrice) / float(prePrice), 4) * 100, 2)
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
            SseData.kline = trend_item

# 异步任务，用于从SSE链接接收数据


async def fetch_sse(url, name=''):
    global session
    if session is not None:
        await session.close()
    session = aiohttp.ClientSession()
    async with session.get(url) as resp:
        async for line in resp.content:
            if line:
                data = line.decode('utf-8')
                data = data[5:] if data.startswith('data:') else data
                data = jsons(data)
                if isinstance(data, dict):
                    json_data = data.get('data', {})
                    handle_sse(json_data, name)


@router.get("/sse/fs/{item}")
async def sse_fs(request: Request, item):
    cancel_task('sse_detail')
    url = 'http://78.push2.eastmoney.com/api/qt/stock/trends2/sse?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f17&fields2=f51,f52,f53,f54,f55,f56,f57,f58&mpi=1000&ut=&secid={}&ndays=1&iscr=0&iscca=0&wbp2u=|0|0|0|web'.format(
        item)
    task = asyncio.create_task(fetch_sse(url, 'kline'))
    task.set_name('sse')
    return {"message": "sse_detail updated"}


@router.get("/sse/kline/{item}")
async def sse_kline(request: Request, item):
    cancel_task('sse_detail')
    url = 'http://78.push2.eastmoney.com/api/qt/stock/trends2/sse?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12,f13,f17&fields2=f51,f52,f53,f54,f55,f56,f57,f58&mpi=1000&ut=&secid={}&ndays=1&iscr=0&iscca=0&wbp2u=|0|0|0|web'.format(
        item)
    task = asyncio.create_task(fetch_sse(url, 'kline'))
    task.set_name('sse')
    return {"message": "sse_detail updated"}


@router.get("/sse/info/get/{item}")
async def sse_info(request: Request, item):
    cancel_task('sse_info')
    # 开始监听新的SSE链接
    fields = ['f58', 'f734', 'f107', 'f57', 'f43', 'f59', 'f169', 'f301', 'f60', 'f170', 'f152', 'f177', 'f111',
              'f46', 'f44', 'f45', 'f47', 'f260', 'f48', 'f261', 'f279', 'f277', 'f278', 'f288', 'f19', 'f17',
              'f531', 'f15', 'f13', 'f11', 'f20', 'f18', 'f16', 'f14', 'f12', 'f39', 'f37', 'f35', 'f33', 'f31',
              'f40', 'f38', 'f36', 'f34', 'f32', 'f211', 'f212', 'f213', 'f214', 'f215', 'f210', 'f209', 'f208',
              'f207', 'f206', 'f161', 'f49', 'f171', 'f50', 'f86', 'f84', 'f85', 'f168', 'f108', 'f116', 'f167',
              'f164', 'f162', 'f163', 'f92', 'f71', 'f117', 'f292', 'f51', 'f52', 'f191', 'f192', 'f262', 'f294',
              'f295', 'f269', 'f270', 'f256', 'f257', 'f285', 'f286', 'f748', 'f747']
    fields = ','.join(fields)
    url = 'http://16.push2.eastmoney.com/api/qt/stock/sse?fields={}&mpi=1000&invt=2&fltt=1&secid={}&ut=&dect=1&wbp2u=|0|0|0|web'.format(
        fields, item)
    task = asyncio.create_task(fetch_sse(url))
    task.set_name('sse')
    return {"message": "sse_info updated"}

# API 端点，用于获取SSE内容


@router.get("/sse/data/{item}")
async def get_sse_data(request: Request, item):
    return StreamingResponse(event_generator(request, item), media_type=media_type)


@router.post("/sse/kline")
async def stock_trend_data(request: Request, item: dict):
    code = item.get('code')
    data = ReqClient.stock_kline(code=code)
    return JSONResponse(status_code=200, content=data)


def cancel_task(name=''):
    name = [name] if name else defaule_name
    tasks = [task for task in asyncio.all_tasks() if task.get_name() in name]
    for task in tasks:
        print('取消 => ', name)
        task.cancel()


async def event_generator(request: Request, func="", stime='', **kwargs):
    md5_code = ""
    data = ""
    stime = stime if stime else sse_time
    while True:
        if func == 'sse_info':
            data = SseData.info
        elif func == 'fs':
            data = SseData.kline
        if isinstance(data, dict) or isinstance(data, list):
            data = json.dumps(data)
        new_md5_code = hashlib.md5(str(data).encode()).hexdigest()
        if md5_code != new_md5_code:
            md5_code = new_md5_code
            yield f"data: {data}\n\n"
        else:
            time.sleep(stime)

        if await request.is_disconnected():
            logger.info("连接已中断")
            cancel_task()
            break
