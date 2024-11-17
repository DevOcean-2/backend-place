"""
즐겨찾기 장소 관련 API
"""
from typing import List

from fastapi import APIRouter, Depends, Query
from fastapi_jwt_auth import AuthJWT
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.schemas.place import PlaceResponse
from app.schemas.favorite import FavoriteAdd, FavoriteList, FavoriteDelete
from app.utils.token import get_social_id
from app.services import favorite as favorite_service

router = APIRouter(
    prefix="/favorites",
    tags=["Place"],
    responses={404: {"description": "Not found"}},
)


@router.post("")
async def add_favorite_place(
        add_req: FavoriteAdd,
        token: AuthJWT = Depends(),
        db: Session = Depends(get_db)):
    """
    장소 즐겨찾기 추가
    :param add_req: 즐찾 추가할 정보
    :param token: JWT 토큰
    :param db:
    :return:
    """
    token.jwt_required()
    user_id = get_social_id(token)

    favorite_service.add_favorite_place(user_id, add_req, db)

    return {"message": "Successfully added a place"}


@router.get("", response_model=List[PlaceResponse])
async def list_favorite_places(
        latitude: float = Query(..., description="위도"),
        longitude: float = Query(..., description="경도"),
        token: AuthJWT = Depends(),
        db: Session = Depends(get_db)):
    """
    즐겨찾기 장소 리스팅
    :param latitude:
    :param longitude:
    :param token:
    :param db:
    :return:
    """
    token.jwt_required()
    user_id = get_social_id(token)

    favorite_list_req = FavoriteList(
        user_id=user_id,
        latitude=latitude,
        longitude=longitude
    )

    return favorite_service.list_favorite_places(favorite_list_req, db)


@router.delete("")
async def delete_favorite_place(
        delete_req: FavoriteDelete,
        token: AuthJWT = Depends(),
        db: Session = Depends(get_db)):
    """
    장소 즐겨찾기 삭제
    :param delete_req:
    :param token: 인증용 토큰
    :param db:
    :return:
    """
    token.jwt_required()
    user_id = get_social_id(token)

    favorite_service.delete_favorite_place(user_id, delete_req, db)

    return {"message": "Successfully deleted a place"}
