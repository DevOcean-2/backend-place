"""
즐겨찾기 장소 관련 API
"""
from typing import List

from fastapi import APIRouter, Depends
from fastapi_jwt_auth import AuthJWT

from app.schemas.place import PlaceResponse
from app.schemas.favorite import FavoriteAdd

router = APIRouter(
    prefix="/favorites",
    tags=["Place"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
async def add_favorite_place(place: FavoriteAdd, token: AuthJWT = Depends()):
    """
    장소 즐겨찾기 추가
    :param place: 즐찾 추가할 정보
    :param token: JWT 토큰
    :return:
    """
    token.jwt_required()

    return {"message": "Successfully added a place"}


@router.get("", response_model=List[PlaceResponse])
async def list_favorite_places(list_name: str, token: AuthJWT = Depends()):
    """
    즐겨찾기 장소 리스팅
    :param list_name: 즐찾 리스트 이름
    :param token:
    :return:
    """

    return None


@router.delete("/{place_id}")
async def delete_favorite_place(place_id: str, token: AuthJWT = Depends()):
    """
    장소 즐겨찾기 삭제
    :param place_id: 장소 id
    :param token: 인증용 토큰
    :return:
    """
    print(place_id, token)
    return {"message": "Successfully deleted a place"}
