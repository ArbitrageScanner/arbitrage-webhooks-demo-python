import asyncio
import datetime
import gzip
import json
import logging
import os
import time

from io import BytesIO
from logging.handlers import TimedRotatingFileHandler

from fastapi import FastAPI, Request, status, APIRouter
from fastapi.responses import JSONResponse

import uvicorn as uvicorn

from models import HookRecord, Spread, Headers

SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = os.getenv('SERVER_PORT', 8181)

os.makedirs("logs", exist_ok=True)

logger = logging.getLogger()
logger.setLevel(logging.INFO)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %Z"
)


# This handler will save app logs directly in file in project folder
file_handler = TimedRotatingFileHandler(
    "logs/app.log",
    when="D",
    interval=1,
    backupCount=7,
    encoding="utf-8"
)
file_handler.setFormatter(formatter)
logger.addHandler(file_handler)

# This is made to have logs in docker as well (as stdout).
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

for uvicorn_logger_name in ("uvicorn", "uvicorn.access", "uvicorn.error"):
    uv_logger = logging.getLogger(uvicorn_logger_name)
    uv_logger.handlers = []
    uv_logger.addHandler(file_handler)
    uv_logger.addHandler(console_handler)
    uv_logger.setLevel(logging.INFO)

app = FastAPI()
router = APIRouter()

class HooksAcceptor:
    def __init__(self):
        self.hooks: dict[str, list[HookRecord]] = {}
        self.lock = asyncio.Lock()

    async def unpack_gzip(self, raw_body: bytes) -> dict | list:
        with gzip.GzipFile(fileobj=BytesIO(raw_body)) as f:
            decompressed_data = f.read()
            decoded_json = json.loads(decompressed_data)
        return decoded_json

    async def accept_hook(self, request: Request, status_code=status.HTTP_200_OK) -> JSONResponse:

        logger.info('Received hook')

        receive_date = int(time.time()*1000)
        receive_date_str = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

        body = await request.body()

        error = None
        success = True

        try:

            decoded_body = await self.unpack_gzip(raw_body=body)
            received_body = [Spread(**spread) for spread in decoded_body.get('data', [])]
            response_date = time.time()

            logger.info('Successfully decoded json.')

        except Exception as err:

            response_date = None
            received_body = []
            error = str(err)
            success = False

            logger.error(f'An error occured: {err}.')

        finally:
            response_body = {
                "success": success,
                "status_code": status_code
            }

        hook_token = request.headers.get('x-hooktoken')

        if not self.hooks.get(hook_token):
            self.hooks[hook_token] = []

        self.hooks[hook_token].append(
            HookRecord(
                hook_token=hook_token,
                receive_date=receive_date,
                receive_date_str=receive_date_str,
                received_body=received_body,
                headers=Headers(**request.headers),
                response_date=response_date,
                response_body=response_body,
                error=error
            )
        )

        logger.info('Saved spreads from hook in RAM. Access via /stats.')

        # For the sake of saving your RAM - we will save only last 10 hooks.
        # If you want to keep all hooks, that are received by server - just delete next two lines.
        async with self.lock:
            self.hooks[hook_token] = self.hooks[hook_token][-10:]

        logger.info('Returning response to hook sender.')
        return JSONResponse(
            status_code=status_code,
            headers={},
            content=response_body
        )

    async def stats(self, request: Request, status_code=status.HTTP_200_OK, hook_token: str = None) -> JSONResponse:

        response_body = {
            "result_status": "success",
            "data": {}
        }

        # If hook_token is specified - only that hook spread batches will be shown in response
        if hook_token:
            response_body['data'][hook_token] = [record.model_dump() for record in self.hooks.get(hook_token, [])]

            logger.info(f'Preparing stats response for a single hook for ip {request.client.host}.')

        # Otherwise - all hooks currently in RAM will be shown
        else:
            for hook in self.hooks:
                response_body['data'][hook] = [record.model_dump() for record in self.hooks.get(hook, [])]

            logger.info(f'Preparing stats response for all hooks for ip {request.client.host}.')


        return JSONResponse(
            status_code=status_code, headers={}, content=response_body
        )


handler = HooksAcceptor()
router.post("/hook")(handler.accept_hook)
router.get("/stats")(handler.stats)
router.get("/stats/{hook_token}")(handler.stats)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("server:app", host=SERVER_IP, port=SERVER_PORT, reload=False)
