import os
import importlib
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from utils.client.redis import lifespan

basedir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) + '/starApi'
default_path = os.path.join(basedir)

app = FastAPI(lifespan=lifespan)  # 添加生命周期为函数 lifespan
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有来源进行跨域请求，您可以根据需求修改为特定的来源列表
    allow_credentials=True,  # 允许携带凭证（例如：cookies）
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)


class ViewFile:
    path = '{}/views'.format(default_path)
    file_names = os.listdir(path)
    modules = [file for file in file_names if '.' and '__' not in file]


class AppSettings:
    for mo in ViewFile.modules:
        path = f'{default_path}/views/{mo}/api/'
        file_names = os.listdir(path)
        modules = [file.rstrip('.py')
                   for file in file_names if not file.startswith('__')]
        for m in modules:
            if m != 'api':
                continue
            imp = f"views.{mo}.api.{m}"
            router_module = importlib.import_module(imp)
            router = getattr(router_module, 'router')
            app.include_router(router)
