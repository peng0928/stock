"""
@ File        : redis.py
@ Version     : V1.0.0
@ Description : redis
"""
from contextlib import asynccontextmanager

from fastapi import FastAPI
from typing import AsyncIterator

from aioredis import from_url, Redis


async def init_redis_pool(host: str, password: str, db: int = 0, port: int = 6379) -> AsyncIterator[Redis]:
    session = await from_url(
        url=f"redis://{host}", port=port, password=password, db=db, encoding="utf-8", decode_responses=True)
    return session


# 关于生命周期事件详见：https://fastapi.tiangolo.com/advanced/events/#lifespan
@asynccontextmanager
async def lifespan(app: FastAPI):
    session = await init_redis_pool(host="127.0.0.1", password="", db=1, port=6379)  # 你的密码<YOU PASSWORD>
    # 将Redis连接添加到app全局实例,详见：https://www.starlette.io/applications/
    # Storing state on the app instance
    app.state.redis = session
    yield
    await session.close()
