"""
Place schema
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl


class PlaceCategory(Enum):
    """
    장소 카테고리
    """
    RESTAURANT = "restaurant"
    CAFE = "cafe"
    BAKERY = "bakery"
    HOSPITAL = "hospital"
    TRAVEL = "travel"
    ETC = "etc"


class PlaceResponse(BaseModel):
    """
    장소 리스폰스 모델
    """
    kakao_place_id: str = Field(..., example="123123")
    kakao_place_url: str = Field(..., example="http://place.map.kakao.com/1459590315")
    name: str = Field(..., example="강아지 병원")
    address: str = Field(..., example="경기 성남시 분당구 대왕판교로 123")
    category: PlaceCategory = Field(..., example=["음식점"])
    distance: int = Field(..., example=10)
    favorite_add_time: Optional[datetime] = Field(..., example=datetime.now())
    image_urls: Optional[List[HttpUrl]] \
        = Field(None, example=[
            "https://test.s3.amazonaws.com/test/test.jpg",
            "https://test.s3.amazonaws.com/test/test2.jpg",
            "https://test.s3.amazonaws.com/test/test3.jpg",])
