"""
장소 관련 API
"""
from typing import List

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.database.db import get_db
from app.schemas.place import PlaceResponse, PlaceList, PlaceKeywordList
from app.services import place as place_service

router = APIRouter(
    prefix="/places",
    tags=["Place"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[PlaceResponse])
async def list_places(list_req: PlaceList,
                      token: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    조건에 맞는 장소 리스팅
    :param list_req:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()

    return place_service.list_places(list_req, db)


@router.get("/keyword/{keyword}", response_model=List[PlaceResponse])
async def list_places_by_keyword(list_req: PlaceKeywordList,
                                 token: AuthJWT = Depends(), db: Session = Depends(get_db)):
    """
    :param list_req:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()

    return place_service.list_places_by_keyword(list_req, db)
