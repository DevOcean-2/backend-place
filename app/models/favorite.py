"""
즐겨찾기 데이터베이스 모델
"""
from datetime import datetime, UTC

from sqlalchemy import Column, Integer, String, Float, DateTime

from app.database.postgres import Base


class Favorite(Base):
    """
    즐겨찾기 테이블
    """
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    list_name = Column(String, nullable=False)
    place_id = Column(String, nullable=False)
    place_name = Column(String, nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(String, nullable=False)
    road_address = Column(String, nullable=True)
    category = Column(String, nullable=False)
    registered_time = Column(DateTime, default=datetime.now(UTC))
