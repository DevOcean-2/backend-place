"""
장소 관련 API
"""
from typing import Optional, List

from fastapi import APIRouter
from pydantic import BaseModel, Field, HttpUrl

router = APIRouter(
    prefix="/places",
    tags=["Place"],
    responses={404: {"description": "Not found"}},
)


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


class Contact(BaseModel):
    """
    연락처 정보
    """
    phone: str = Field(..., example="010-1234-1234")
    site: HttpUrl = Field(..., example="sk.co.kr")
    email: str = Field(..., example="example@example.com")


class PlaceResp(BaseModel):
    """
    장소 리스폰스 모델
    """
    id: str = Field(..., example="123123")
    name: str = Field(..., example="강아지 병원")
    address: str = Field(..., example="경기 성남시 분당구 대왕판교로 123")
    category: List[str] = Field(..., example=["병원", "약국"])
    distance: int = Field(..., example=10)
    images: Optional[List[HttpUrl]] \
        = Field(None, example=[
            "https://test.s3.amazonaws.com/test/test.jpg",
            "https://test.s3.amazonaws.com/test/test2.jpg",
            "https://test.s3.amazonaws.com/test/test3.jpg",])


class PlaceInfoResp(PlaceResp):
    """
    장소 상세 리스폰스 모델
    """
    business_hours: BusinessHours
    is_certified: bool = Field(False, example=True)
    contacts: Contact


@router.get("", response_model=List[PlaceResp])
async def list_places(category:str, location:str, offset:int):
    """
    조건에 맞는 장소 리스팅
    :param category: 리스팅할 장소의 카테고리
    :param location: 설정한 위치
    :param offset: 얼마나 떨어진 장소까지 리스팅 할지
    :return:
    """
    print(category, location, offset)
    return None


@router.get("/{place_id}", response_model=PlaceInfoResp)
async def get_place_info(place_id: str):
    """
    장소 상세 정보 반환
    :param place_id: 장소 id
    :return:
    """
    print(place_id)
    return None


@router.get("/recommendation", response_model=List[PlaceResp])
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


@router.post("/favorites")
async def add_favorite_place(place_id: str, token: str):
    """
    장소 즐겨찾기 추가
    :param place_id: 장소 id
    :param token: 인증용 토큰
    :return:
    """
    print(place_id, token)
    return {"message": "Successfully added a place"}


@router.get("/favorites", response_model=List[PlaceResp])
async def list_favorite_places(token: str):
    """
    즐겨찾기 장소 리스팅
    :param token:
    :return:
    """
    print(token)
    return None


@router.delete("/favorites/{place_id}")
async def delete_favorite_place(place_id: str, token: str):
    """
    장소 즐겨찾기 삭제
    :param place_id: 장소 id
    :param token: 인증용 토큰
    :return:
    """
    print(place_id, token)
    return {"message": "Successfully deleted a place"}
