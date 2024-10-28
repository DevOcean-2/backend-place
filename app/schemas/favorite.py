from pydantic import BaseModel


class FavoriteAdd(BaseModel):
    """
    즐겨찾기
    """
    place_id: str
    favorite_list_name: str
