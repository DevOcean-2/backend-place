"""
main.py
"""

import logging
import os
import uuid

from fastapi import FastAPI, APIRouter
from fastapi_jwt_auth import AuthJWT
from pydantic import BaseModel
from starlette_context import context
from starlette_context.middleware import ContextMiddleware
from starlette.responses import Response

from app.routers import place, favorite

logger = logging.getLogger(__name__)


class Settings(BaseModel):
    """
    AuthJWT config setting
    """
    authjwt_secret_key: str = os.getenv("JWT_SECRET_KEY")


@AuthJWT.load_config
def get_config():
    """
    AuthJWT config
    """
    return Settings()


# fastAPI app 생성
app = FastAPI(
    title="Balbalm Place Backend",
    description="backend for balbalm place service",
    version="1.0-beta",
    openapi_url="/place/openapi.json",
    docs_url="/place/docs",
    redoc_url="/place/redoc",
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


# place prefix 추가
place_router = APIRouter(
    prefix="/place",
    tags=["Place"]
)


# app 에 상세 router 추가
place_router.include_router(place.router)
place_router.include_router(favorite.router)

app.include_router(place_router)
