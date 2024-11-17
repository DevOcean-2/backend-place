"""
즐겨찾기 서비스 로직
"""
from datetime import datetime
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError

from app.database.opensearch import get_document
from app.schemas.favorite import (FavoriteListResponse,
                                  FavoriteList, FavoritePlaceDetail, FavoriteAdd, FavoriteDelete)
from app.models.favorite import Favorite as FavoriteTable
from app.utils.coordinate import calculate_place_distance


def add_favorite_place(user_id: str, add_req: FavoriteAdd, db: Session) -> None:
    """
    즐겨찾기 추가 로직
    :param user_id:
    :param add_req:
    :param db:
    :return:
    """
    place = get_document("places", add_req.place_id)
    favorite_place = FavoriteTable(
        user_id=user_id,
        list_name=add_req.favorite_list_name,
        place_id=add_req.place_id,
        latitude=place['location']['lat'],
        longitude=place['location']['lon'],
        address=place['address'],
        road_address=place['road_address'],
        category=place['category'],
        registerd_time=datetime.now()
    )

    try:
        db.add(favorite_place)
        db.commit()
        db.refresh(favorite_place)
    except IntegrityError:
        db.rollback()
        raise


def list_favorite_places(favorite_list_req: FavoriteList, db: Session) \
        -> List[FavoriteListResponse]:
    """
    즐겨찾기 장소 리스팅 로직
    :param favorite_list_req:
    :param db:
    :return:
    """
    favorites: List[FavoriteTable] = (
        db.query(FavoriteTable).filter(FavoriteTable.user_id == favorite_list_req.user_id).all())

    favorite_places: dict[str, List[FavoritePlaceDetail]] = {}

    lat = favorite_list_req.latitude
    lon = favorite_list_req.longitude
    for favorite in favorites:
        if favorite.list_name not in favorite_places:
            favorite_places[favorite.list_name] = []
        favorite_places[favorite.list_name].append(
            FavoritePlaceDetail(
                place_id=favorite.place_id,
                address=favorite.address,
                distance=calculate_place_distance(lat, lon, favorite.latitude, favorite.longitude),
                road_address=favorite.road_address,
                category=favorite.category,
                registered_time=favorite.registered_time
            )
        )

    favorite_response = []
    for list_name, places in favorite_places.items():
        favorite_response.append(FavoriteListResponse(favorite_list_name=list_name, places=places))

    return favorite_response


def delete_favorite_place(user_id: str, delete_req: FavoriteDelete, db: Session) -> None:
    """
    즐겨찾기 삭제 로직
    :param user_id:
    :param delete_req:
    :param db:
    :return:
    """
    favorites: List[FavoriteTable] = (
        db.query(FavoriteTable)
        .filter(FavoriteTable.user_id == user_id,
                FavoriteTable.list_name == delete_req.favorite_list_name).all())

    for favorite in favorites:
        if favorite.place_id in delete_req.place_ids:
            try:
                db.delete(favorite)
                db.commit()
            except IntegrityError:
                db.rollback()
                raise
