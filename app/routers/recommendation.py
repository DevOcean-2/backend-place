"""
추천 장소 관련 API
"""
from typing import List

from fastapi import APIRouter

from app.schemas.place import PlaceResponse

router = APIRouter(
    prefix="/recommendations",
    tags=["Place"],
    responses={404: {"description": "Not found"}},
)


@router.get("", response_model=List[PlaceResponse])
async def list_recommend_places(category: str, location: str, offset: int):
    """
    조건에 맞는 추천 장소 리스팅
    :param category: 리스팅할 장소의 카테고리
    :param location: 설정한 위치
    :param offset: 얼마나 떨어진 장소까지 리스팅 할지
    :return:
    """
    print(category, location, offset)
    return None
