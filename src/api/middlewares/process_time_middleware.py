import time

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware

from ...core.headers import Headers


class ProcessTimeMiddleware(BaseHTTPMiddleware):
    async def dispatch(
        self,
        request: Request,
        call_next,
    ):
        start_time = time.time()
        response = await call_next(request)
        process_time = time.time() - start_time
        response.headers[Headers.X_PROCESS_TIME_HEADER] = str(process_time)
        return response
