"""
장소 데이터베이스 모델
"""
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.dialects.postgresql import JSONB

from app.database.db import Base


class Place(Base):
    """
    장소 테이블
    """
    __tablename__ = "places"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    address_name = Column(String, nullable=False)
    category_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    image_urls = Column(JSONB)

    kakao_place_id = Column(String, unique=True, index=True, nullable=False)
    kakao_place_url = Column(String, nullable=False)
