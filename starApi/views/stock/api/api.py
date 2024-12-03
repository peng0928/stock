from fastapi import *
from fastapi.routing import APIRouter
from fastapi.responses import ORJSONResponse, JSONResponse

from utils.ticket.request.api import *
from views.stock.model.index import *

ReqClient = RequestClient()

router = APIRouter(
    prefix="/api",
    tags=["订单"],
    default_response_class=ORJSONResponse
)


@router.post("/stock/get")
async def stock_get(request: Request, item: StockItem):
    data = ReqClient.stock_get(code=item.code)
    return JSONResponse(status_code=200, content=data)


@router.post("/stock/trend")
async def stock_trend(request: Request, item: StockTrend):
    hy = item.hy
    dp = item.dp
    code = item.code
    hy_data = ReqClient.stock_trends2(code=hy)
    dp_data = ReqClient.stock_trends2(code=dp)
    data = [hy_data, dp_data]
    bk_data = ReqClient.stock_securities(code=code)
    if bk_data:
        for item in bk_data:
            data.append(item)
    return JSONResponse(status_code=200, content=data)


@router.post("/stock/trend/data")
async def stock_trend_data(request: Request, item: StockItem):
    code = item.code
    data = ReqClient.stock_trends(code=code)
    return JSONResponse(status_code=200, content=data)
