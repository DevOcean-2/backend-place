"""
즐겨찾기 장소 관련 API
"""
from typing import List

from fastapi import APIRouter

from app.schemas.place import PlaceResponse

router = APIRouter(
    prefix="/favorites",
    tags=["Place"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
async def add_favorite_place(place_id: str, token: str):
    """
    장소 즐겨찾기 추가
    :param place_id: 장소 id
    :param token: 인증용 토큰
    :return:
    """
    print(place_id, token)
    return {"message": "Successfully added a place"}


@router.get("", response_model=List[PlaceResponse])
async def list_favorite_places(token: str):
    """
    즐겨찾기 장소 리스팅
    :param token:
    :return:
    """
    print(token)
    return None


@router.delete("/{place_id}")
async def delete_favorite_place(place_id: str, token: str):
    """
    장소 즐겨찾기 삭제
    :param place_id: 장소 id
    :param token: 인증용 토큰
    :return:
    """
    print(place_id, token)
    return {"message": "Successfully deleted a place"}
