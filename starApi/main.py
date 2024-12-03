import uvicorn
from settions import *
from uvicorn.config import LOGGING_CONFIG

LOGGING_CONFIG["formatters"]["default"]["fmt"] = "%(asctime)s - %(levelprefix)s %(message)s"
LOGGING_CONFIG["formatters"]["access"][
    "fmt"] = "%(asctime)s - %(levelprefix)s %(client_addr)s - \"%(request_line)s\" %(status_code)s"

if __name__ == '__main__':
    uvicorn.run(app='main:app', host='0.0.0.0', port=6888, workers=1)
