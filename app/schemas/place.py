"""
Place schema
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl
from fastapi import Query

from app.utils.kakaomap import SearchResultSortType


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


class DailyOpeningHours(BaseModel):
    """
    하루 영업 시간 모델
    """
    open_time: str = Field(..., example="09:00")
    close_time: str = Field(..., example="18:00")
    is_open: Optional[bool] = Field(None, example=True)


class BusinessHours(BaseModel):
    """
    일주일 영업 시간 모델
    """
    mon: Optional[DailyOpeningHours] \
        = Field(None, examples=[{"open_time": "09:00", "close_time": "18:00", "is_open": True}])
    tue: Optional[DailyOpeningHours] \
        = Field(None, examples=[{"open_time": "09:00", "close_time": "18:00", "is_open": True}])
    wed: Optional[DailyOpeningHours] \
        = Field(None, examples=[{"open_time": "09:00", "close_time": "18:00", "is_open": True}])
    thu: Optional[DailyOpeningHours] \
        = Field(None, examples=[{"open_time": "09:00", "close_time": "18:00", "is_open": True}])
    fri: Optional[DailyOpeningHours] \
        = Field(None, examples=[{"open_time": "09:00", "close_time": "18:00", "is_open": True}])
    sat: Optional[DailyOpeningHours] \
        = Field(None, examples=[{"open_time": "09:00", "close_time": "14:00", "is_open": True}])
    sun: Optional[DailyOpeningHours] \
        = Field(None, examples=[{"open_time": "휴무", "close_time": "휴무", "is_open": False}])


class PlaceList(BaseModel):
    """
    장소 리스팅 리퀘스트 모델
    """
    latitude: float = Query(..., description="위도")
    longitude: float = Query(..., description="경도")
    category: Optional[PlaceCategory] = Query(None, description="카테고리")


class PlaceKeywordList(BaseModel):
    """
    키워드 기반 장소 리퀘스트 모델
    """
    latitude: float
    longitude: float
    keyword: str
    sort_by: SearchResultSortType = Field(SearchResultSortType.SORT_TYPE_ACCURACY)


class PlaceResponse(BaseModel):
    """
    장소 리스폰스 모델
    """
    place_id: str = Field(...)
    name: str = Field(..., example="강아지 병원")
    address: str = Field(..., example="경기 성남시 분당구 대왕판교로 123")
    category: PlaceCategory = Field(..., example=["restaurant"])
    distance: int = Field(..., example=10)
    image_urls: Optional[List[HttpUrl]] \
        = Field(None, example=[
            "https://test.s3.amazonaws.com/test/test.jpg",
            "https://test.s3.amazonaws.com/test/test2.jpg",
            "https://test.s3.amazonaws.com/test/test3.jpg",])
    opening_hours: Optional[BusinessHours] = Field(None)
    phone_number: Optional[str] = Field(None, example="010-1234-5678")
    website_url: Optional[str] = Field(None, example="http://place.map.kakao.com/1459590315")
    favorite_add_time: Optional[datetime] = Field(None, example=datetime.now())
