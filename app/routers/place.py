"""
장소 관련 API
"""
from typing import List, Optional

from fastapi import APIRouter, Depends, Query
from fastapi_jwt_auth import AuthJWT

from app.schemas.place import PlaceResponse, PlaceList
from app.services import place as place_service

router = APIRouter(
    prefix="/places",
    tags=["Place"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[PlaceResponse])
async def list_places(
        latitude: float = Query(..., description="위도"),
        longitude: float = Query(..., description="경도"),
        category: Optional[str] = Query(None, description="선택적 카테고리 필터"),
        token: AuthJWT = Depends()
    ):
    """
    조건에 맞는 장소 리스팅
    :param latitude:
    :param longitude:
    :param category:
    :param token:
    :return:
    """
    token.jwt_required()
    list_req = PlaceList(
        latitude=latitude,
        longitude=longitude,
        category=category
    )

    return place_service.list_places(list_req)


# @router.get("/keyword/{keyword}", response_model=List[PlaceResponse])
# async def list_places_by_keyword(list_req: PlaceKeywordList,
#                                  token: AuthJWT = Depends(), db: Session = Depends(get_db)):
#     """
#     :param list_req:
#     :param token:
#     :param db:
#     :return:
#     """
#     token.jwt_required()
#
#     return place_service.list_places_by_keyword(list_req, db)
