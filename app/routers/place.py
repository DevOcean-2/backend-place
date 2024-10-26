"""
장소 관련 API
"""
from typing import List

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from app.schemas.place import PlaceResponse, PlaceInfoResponse

router = APIRouter(
    prefix="/places",
    tags=["Place"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[PlaceResponse])
async def list_places(category: str, location: str, offset: int, token: AuthJWT = Depends()):
    """
    조건에 맞는 장소 리스팅
    :param category: 리스팅할 장소의 카테고리
    :param location: 설정한 위치
    :param offset: 얼마나 떨어진 장소까지 리스팅 할지
    :param token:
    :return:
    """
    token.jwt_required()
    print(category, location, offset)
    return None


@router.get("/{place_id}", response_model=PlaceInfoResponse)
async def get_place_info(place_id: str, token: AuthJWT = Depends()):
    """
    장소 상세 정보 반환
    :param place_id: 장소 id
    :param token:
    :return:
    """
    token.jwt_required()
    print(place_id)
    return None
