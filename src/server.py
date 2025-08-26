import asyncio
import datetime
import logging
import os
import time
from collections import defaultdict, deque

from logging.handlers import TimedRotatingFileHandler
from typing import DefaultDict, Deque

from fastapi import FastAPI, Request, status, APIRouter
from fastapi.responses import JSONResponse

import uvicorn as uvicorn

from src.models import HookRecord, Spread, Headers
from src.utils import unpack_gzip

SERVER_IP = os.getenv('SERVER_IP')
SERVER_PORT = os.getenv('SERVER_PORT', 8000)
LOGGING_LEVEL = os.getenv('LOGGING_LEVEL', 'INFO')

os.makedirs("../logs", exist_ok=True)

logger = logging.getLogger()
logger.setLevel('INFO')

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S %Z"
)

# This handler will save app logs directly in file in project folder
file_handler = TimedRotatingFileHandler(
    "../logs/app.log",
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
    """
    Class representing hooks requests receiving and management.
    Consists of accept_hook, which will process incoming POST-requests and process it, and stats method, which returns saved spread batches, depending on whether hook_token is passed or not.

    You can also add your own methods in this class directly, just don't forget to add them to router.

    You can also add your own endpoints in three ways:
    1.) add new class methods directly in this class
    2.) create your own class
    3.) create static functions

    First two ways can be realized using following code:

    router = ApiRouter() # a router instance

    class SomeClass:
        async def some_method(self):


    """
    def __init__(
            self,
            cache_width: int = 10
    ):
        self.hooks: DefaultDict[str, Deque[HookRecord]] = defaultdict(lambda: deque(maxlen=cache_width))
        self.lock = asyncio.Lock()

    async def accept_hook(
            self,
            request: Request,
            status_code: int = status.HTTP_200_OK
    ) -> JSONResponse:
        """
        Tries to decompress gzip-packed json-serialized data, create a pydantic model out of it, saves it to cache and return a json-response.
        By default, saves in cache only last 10 hooks.

        :param request: received request
        :type request: fastapi.Request
        :param status_code: status code to return, defaults to 200
        :type status_code: int
        :return: JsonResponse object
        :rtype: fastapi.responses.JSONResponse
        """

        logger.info('Received hook')

        receive_date = int(time.time()*1000)
        receive_date_str = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

        body = await request.body()

        error = None
        success = True

        try:

            decoded_body = await unpack_gzip(raw_body=body)
            received_body = [
                Spread(**spread) for spread in decoded_body.get('data', [])
            ]
            headers = Headers(**request.headers)
            response_date = time.time()

            logger.info('Successfully decoded json.')

        except Exception as err:

            response_date = None
            received_body = []
            headers = None
            error = str(err)
            success = False

            status_code = status.HTTP_500_INTERNAL_SERVER_ERROR

            logger.error(f'An error occurred: {err}.')

        finally:
            response_body = {
                "success": success,
                "status_code": status_code
            }

        hook_token = request.headers.get('x-hooktoken')

        self.hooks[hook_token].append(
            HookRecord(
                hook_token=hook_token,
                receive_date=receive_date,
                receive_date_str=receive_date_str,
                received_body=received_body,
                headers=headers,
                response_date=response_date,
                response_body=response_body,
                error=error
            )
        )

        logger.info(f'Saved spreads from hook with hook_token {hook_token} in RAM. Access via /stats.')


        logger.info('Returning response to hook sender.')

        return JSONResponse(
            status_code=status_code,
            headers={},
            content=response_body
        )

    async def stats(self, request: Request, status_code=status.HTTP_200_OK, hook_token: str = None) -> JSONResponse:
        """
        Returns a JsonResponse, containing received data from a webhooks, depending on passing hook_token value.
        If hook_token is passed - tries to find in cache and return all records with passed hook_token.
        Otherwise - returns everything currently stored in cache.

        :param request: received request
        :type request: fastapi.Request
        :param status_code: status code to return, defaults to 200
        :type status_code: int
        :param hook_token: a unique hook identifier, can be found either in received request headers (which is also included in response from this method) or in hooks list from GET-method or web-interface, defaults to None
        :type hook_token: str
        :return: JsonResponse object, containing all found data
        :rtype: fastapi.responses.JSONResponse
        """
        response_body = {
            "result_status": "success",
            "data": {}
        }

        # If hook_token is specified - only that hook spread batches will be shown in response
        if hook_token:
            response_body['data'][hook_token] = [
                record.model_dump() for record in self.hooks.get(hook_token, [])
            ]

            logger.info(f'Preparing stats response for a single hook for ip {request.client.host}.')

        # Otherwise - all hooks currently in RAM will be shown
        else:
            for hook in self.hooks:
                response_body['data'][hook] = [
                    record.model_dump() for record in self.hooks.get(hook, [])
                ]

            response_body['data'] = {
                hook:[
                    record.model_dump() for record in self.hooks.get(hook, [])
                ] for hook in self.hooks
            }

            logger.info(f'Preparing stats response for all hooks for ip {request.client.host}.')


        return JSONResponse(
            status_code=status_code,
            headers={},
            content=response_body
        )


handler = HooksAcceptor()
router.post("/hook")(handler.accept_hook)
router.get("/stats")(handler.stats)
router.get("/stats/{hook_token}")(handler.stats)

app.include_router(router)

if __name__ == '__main__':
    uvicorn.run("server:app", host=SERVER_IP, port=int(SERVER_PORT), reload=False)