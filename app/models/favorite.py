"""
즐겨찾기 데이터베이스 모델
"""
from sqlalchemy import Column, Integer, String, ForeignKey

from app.database.db import Base


class Favorite(Base):
    """
    즐겨찾기 테이블
    """
    __tablename__ = "favorite_places"

    id = Column(Integer, primary_key=True, index=True)
    list_name = Column(String, index=True, nullable=False)
    user_id = Column(String, index=True, nullable=False)
    kakao_place_id = Column(String, ForeignKey('places.kakao_place_id'), nullable=False)
