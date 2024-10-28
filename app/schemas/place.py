"""
Place schema
"""
from datetime import datetime
from enum import Enum
from typing import Optional, List

from pydantic import BaseModel, Field, HttpUrl


class PlaceCategory(Enum):
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


# class Contact(BaseModel):
#     """
#     연락처 정보
#     """
#     phone: str = Field(..., example="010-1234-1234")
#     site: HttpUrl = Field(..., example="sk.co.kr")
#     email: str = Field(..., example="example@example.com")


class PlaceResponse(BaseModel):
    """
    장소 리스폰스 모델
    """
    id: str = Field(..., example="123123")
    name: str = Field(..., example="강아지 병원")
    address: str = Field(..., example="경기 성남시 분당구 대왕판교로 123")
    category: List[PlaceCategory] = Field(..., example=["음식점", "카페"])
    distance: int = Field(..., example=10)
    business_hours: BusinessHours
    favorite_add_time: Optional[datetime] = Field(..., example=datetime.now())
    images: Optional[List[HttpUrl]] \
        = Field(None, example=[
            "https://test.s3.amazonaws.com/test/test.jpg",
            "https://test.s3.amazonaws.com/test/test2.jpg",
            "https://test.s3.amazonaws.com/test/test3.jpg",])


# class PlaceInfoResponse(PlaceResponse):
#     """
#     장소 상세 리스폰스 모델
#     """
#     business_hours: BusinessHours
#     is_certified: bool = Field(False, example=True)
#     contacts: Contact
