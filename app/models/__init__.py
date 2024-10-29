"""
models
"""
from sqlalchemy.orm import relationship

from app.models.favorite import Favorite
from app.models.place import Place

Place.favorites = relationship("Favorite", back_populates="place")
Favorite.place = relationship("Place", back_populates="favorites")
