"""
main.py
"""

import logging
import uuid

from fastapi import FastAPI
from starlette.responses import Response
from starlette_context import context
from starlette_context.middleware import ContextMiddleware
from routers import place

logger = logging.getLogger(__name__)

# fastAPI app 생성
app = FastAPI(
    title="Balbalm Feed Backend",
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


@app.get("/place", response_model=dict)
async def get_place_apis():
    """
    place 관련 모든 api 리스팅
    :return:
    """
    return {
        "message": "Welcome to the Balbalm Place API!",
        "endpoints": {
            "GET /places": "Get place list nearby",
            "GET /places/{place_id}": "Get a place info",
            "GET /places/recommendation": "Get recommended place list",
            "POST /places/favorites": "Add to my favorite place list",
            "DELETE /places/favorites/{place_id}": "Delete a place from favorite place list",
            "GET /places/favorites": "List my favorite places"
        }
    }


# app 에 상세 router 추가
app.include_router(place.router)
