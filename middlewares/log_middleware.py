import logging
import time
from fastapi import Request

logger = logging.getLogger("request")


class RequestLoggingMiddleware:
    async def __call__(self, request: Request, call_next):
        start_time = time.time()

        response = await call_next(request)

        process_time = time.time() - start_time

        logger.info(
            "%s %s | status=%s | time=%.3fs | ip=%s",
            request.method,
            request.url.path,
            response.status_code,
            process_time,
            request.client.host if request.client else "unknown"
        )

        return response
