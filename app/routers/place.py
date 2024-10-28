"""
장소 관련 API
"""
from typing import List, Optional

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from app.schemas.place import PlaceResponse, PlaceCategory
from app.utils.kakaomap import SearchResultSortType

router = APIRouter(
    prefix="/places",
    tags=["Place"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[PlaceResponse])
async def list_places(
        latitude: float,
        longitude: float,
        category: PlaceCategory,
        keyword: Optional[str] = None,
        sort_by: Optional[SearchResultSortType] = SearchResultSortType.SORT_TYPE_ACCURACY,
        token: AuthJWT = Depends()):
    """
    조건에 맞는 장소 리스팅
    :param latitude: 위도
    :param longitude: 경도
    :param category: 리스팅할 장소의 카테고리 (restaurant, cafe, bakery, hospital, travel, etc)
    :param keyword: 검색 키워드
    :param sort_by: 거리순/정확도순 (accuracy, distance)
    :param token:
    :return:
    """
    token.jwt_required()

    return None


# @router.get("/{place_id}", response_model=PlaceInfoResponse)
# async def get_place_info(place_id: str, token: AuthJWT = Depends()):
#     """
#     장소 상세 정보 반환
#     :param place_id: 장소 id
#     :param token:
#     :return:
#     """
#     token.jwt_required()
#     print(place_id)
#     return None
