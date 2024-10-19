"""
main.py
"""

import logging
import uuid

from fastapi import FastAPI, APIRouter
from starlette.responses import Response
from starlette_context import context
from starlette_context.middleware import ContextMiddleware

from app.routers import place, recommendation, favorite

logger = logging.getLogger(__name__)

# fastAPI app 생성
app = FastAPI(
    title="Balbalm Place Backend",
    description="backend for balbalm place service",
    version="1.0-beta",
    openapi_url="/openapi.json",
)

app.logger = logger


@app.middleware("http")
async def http_log(request, call_next):
    """
    로그
    :param request:
    :param call_next:
    :return:
    """
    response = await call_next(request)
    response_body = b''
    log_uuid = str(uuid.uuid1())[:8]
    # Combine async response chunk
    async for chunk in response.body_iterator:
        response_body += chunk
    logger.info("Log ID : %s - Request URL : %s %s",
                log_uuid, str(request.method), str(request.url))
    if "request_body" in context:
        logger.info("Log ID : %s - Request Body : %s", log_uuid, context["request_body"])
    logger.info("Log ID : %s - Response Body : %s", log_uuid, response_body)
    logger.info("Log ID : %s - Response Status Code : %s", log_uuid, str(response.status_code))

    return Response(
        content=response_body,
        status_code=response.status_code,
        headers=dict(response.headers),
        media_type=response.media_type
    )

app.add_middleware(ContextMiddleware)

# TODO: Auth 추가

# place prefix 추가
place_router = APIRouter(
    prefix="/place",
    tags=["Place"]
)


# app 에 상세 router 추가
place_router.include_router(place.router)
place_router.include_router(recommendation.router)
place_router.include_router(favorite.router)

app.include_router(place_router)