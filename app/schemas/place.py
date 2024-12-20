"""
Place schema
"""
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl
from fastapi import Query


class PlaceListSortType(Enum):
    """
    장소 키워드 검색 시 정렬 방법
    """
    SORT_TYPE_ACCURACY = "accuracy"
    SORT_TYPE_DIST = "distance"


class PlaceCategory(Enum):
    """
    장소 카테고리
    """
    RESTAURANT = "restaurant"
    CAFE = "cafe"
    HOSPITAL = "hospital"
    CULTURE = "culture"
    ETC = "etc"


class DailyOpeningHours(BaseModel):
    """
    하루 영업 시간 모델
    """
    open_time: str = Field(..., example="09:00")
    close_time: str = Field(..., example="18:00")
    is_open: Optional[bool] = Field(None, example=True)

# 현재 가져오는 데이터에서 분류 불가.
# class BusinessHours(BaseModel):
#     """
#     일주일 영업 시간 모델
#     """
#     mon: Optional[DailyOpeningHours] \
#         = Field(None, examples=[{"open_time": "09:00", "close_time": "18:00", "is_open": True}])
#     tue: Optional[DailyOpeningHours] \
#         = Field(None, examples=[{"open_time": "09:00", "close_time": "18:00", "is_open": True}])
#     wed: Optional[DailyOpeningHours] \
#         = Field(None, examples=[{"open_time": "09:00", "close_time": "18:00", "is_open": True}])
#     thu: Optional[DailyOpeningHours] \
#         = Field(None, examples=[{"open_time": "09:00", "close_time": "18:00", "is_open": True}])
#     fri: Optional[DailyOpeningHours] \
#         = Field(None, examples=[{"open_time": "09:00", "close_time": "18:00", "is_open": True}])
#     sat: Optional[DailyOpeningHours] \
#         = Field(None, examples=[{"open_time": "09:00", "close_time": "14:00", "is_open": True}])
#     sun: Optional[DailyOpeningHours] \
#         = Field(None, examples=[{"open_time": "휴무", "close_time": "휴무", "is_open": False}])


class PlaceList(BaseModel):
    """
    장소 리스팅 리퀘스트 모델
    """
    latitude: float = Query(..., description="위도")
    longitude: float = Query(..., description="경도")
    category: Optional[PlaceCategory] = Query(None, description="카테고리")
    sort_by: Optional[PlaceListSortType] = Query(PlaceListSortType.SORT_TYPE_ACCURACY)


class PlaceKeywordList(BaseModel):
    """
    키워드 기반 장소 리퀘스트 모델
    """
    latitude: float
    longitude: float
    keyword: str
    sort_by: Optional[PlaceListSortType] = Query(PlaceListSortType.SORT_TYPE_ACCURACY)


class PlaceResponse(BaseModel):
    """
    장소 리스폰스 모델
    """
    place_id: str = Field(...)
    name: str = Field(..., example="강아지 병원")
    address: str = Field(..., example="서울 서초구 매헌로16길 24")
    road_address: str = Field(..., example="경기 성남시 분당구 대왕판교로 123")
    category: PlaceCategory = Field(..., example=["restaurant"])
    distance: int = Field(..., example=10)
    image_urls: Optional[List[HttpUrl]] \
        = Field(None, example=[
            "https://test.s3.amazonaws.com/test/test.jpg",
            "https://test.s3.amazonaws.com/test/test2.jpg",
            "https://test.s3.amazonaws.com/test/test3.jpg",])
    opening_hours: Optional[List[str]] = Field(
        None,
        example=[
            "월~금 08:00 ~ 19:00",
            "토,일 11:00 ~ 19:00",
            "공휴일 11:00 ~ 19:00"
        ]
    )
    phone_number: Optional[str] = Field(None, example="010-1234-5678")
    website_url: Optional[str] = Field(None, example="http://place.map.kakao.com/1459590315")
