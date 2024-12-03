from datetime import datetime, timezone, timedelta

from fastapi.responses import ORJSONResponse, JSONResponse
from fastapi.routing import APIRouter
from fastapi import *
from fastapi.responses import HTMLResponse
from utils.ticket.request.api import *

from utils.ticket.request.tool.ticket_tool import request_set_cookie

ReqClient = RequestClient()
router = APIRouter(
    prefix="/api",
    tags=["登录"],
    default_response_class=ORJSONResponse
)


@router.get("/create-qr64")
async def CreateQr(request: Request):
    data, get_cookie = ReqClient.create_qr(cookie=request.cookies)
    response = JSONResponse(status_code=200, content=data)
    expires = datetime.now(timezone.utc) + timedelta(days=30)  # 设置过期时间
    response = request_set_cookie(response, get_cookie, expires)
    return response


@router.get("/iconfont")
async def iconfont(request: Request):
    get_cookie, code = ReqClient.iconfont(cookie=request.cookies)
    response = JSONResponse(status_code=200, content={"code": code})
    expires = datetime.now(timezone.utc) + timedelta(days=30)  # 设置过期时间
    response = request_set_cookie(response, get_cookie, expires)
    return response


@router.post("/check-qr")
async def CheckQr(request: Request, item: dict):
    data = ReqClient.check_qr(cookie=request.cookies, **item)
    return JSONResponse(status_code=200, content=data)


@router.post("/login")
async def login(item: dict, request: Request):
    print(item)
    data, get_cookie = ReqClient.login(**item)
    status = data.get("status")
    msg = data.get("msg")
    if status:
        cookie_data = data.get('data')
        uKey = cookie_data.get('uKey')
        tk = cookie_data.get('tk')
        response = JSONResponse(status_code=200, content={"status": status, "msg": msg})
        expires = datetime.now(timezone.utc) + timedelta(days=30)  # 设置过期时间
        response.set_cookie(key="uKey", value=uKey, expires=expires, secure=False, httponly=True)
        response.set_cookie(key="tk", value=tk, expires=expires, secure=False, httponly=True)
        response = request_set_cookie(response, get_cookie, expires)
        await request.app.state.redis.set('cookie:{}', json.dumps(get_cookie or {}))
        return response
    else:
        return JSONResponse(status_code=400, content={"status": status, "msg": msg})


@router.post("/check/user")
async def CheckUser(request: Request):
    data = ReqClient.check_user(cookie=request.cookies)
    return JSONResponse(status_code=200, content=data)


@router.get("/get/user")
async def getUser(request: Request):
    data = ReqClient.get_user(cookie=request.cookies)
    return JSONResponse(status_code=200, content=data)
