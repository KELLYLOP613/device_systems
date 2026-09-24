import logging
import time
import uuid

from fastapi import Request

logger = logging.getLogger("device_systems")


async def custom_request_middleware(request: Request, call_next):
    start_time = time.perf_counter()

    request_id = request.headers.get("X-Request-ID", str(uuid.uuid4()))
    request.state.request_id = request_id

    response = await call_next(request)

    process_time = time.perf_counter() - start_time

    response.headers["X-Process-Time"] = f"{process_time:.4f}"
    response.headers["X-App-Name"] = "device_systems"
    response.headers["X-Request-ID"] = request_id

    logger.info(
        "%s %s -> %s | request_id=%s | process_time=%.4fs",
        request.method,
        request.url.path,
        response.status_code,
        request_id,
        process_time,
    )

    return response