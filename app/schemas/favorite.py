"""
즐겨찾기 스키마
"""
from datetime import datetime
from typing import List

from pydantic import BaseModel
from app.schemas.place import PlaceCategory


class FavoriteAdd(BaseModel):
    """
    즐겨찾기 추가 리퀘스트
    """
    place_id: str
    favorite_list_name: str


class FavoriteDelete(BaseModel):
    """
    즐겨찾기 삭제 리퀘스트
    """
    favorite_list_name: str
    place_ids: List[str]


class FavoriteList(BaseModel):
    """
    즐겨찾기 장소 리스팅 리퀘스트
    """
    user_id: str
    latitude: float
    longitude: float


class FavoritePlaceDetail(BaseModel):
    """
    즐겨찾기 장소 디테일
    """
    place_id: str
    place_name: str
    distance: int
    address: str
    road_address: str
    category: PlaceCategory
    registered_time: datetime


class FavoriteListResponse(BaseModel):
    """
    즐겨찾기 장소 리스폰스 모델
    """
    favorite_list_name: str
    places: List[FavoritePlaceDetail]
