"""
장소 서비스 로직
"""
from typing import List

from sqlalchemy import func
from sqlalchemy.orm import Session

from app.schemas.place import PlaceResponse, PlaceList, PlaceKeywordList
from app.models.place import Place as PlaceTable
from app.utils.coordinate import calculate_place_distance
from app.utils.kakaomap import get_places_with_keyword, SearchKeywordParams


def list_places(list_req: PlaceList, db: Session) -> List[PlaceResponse]:
    """
    장소 리스팅 로직
    :param list_req: 
    :param db: 
    :return: 
    """
    place_list_resp: List[PlaceResponse] = []
    query = list_places_in_target_radius(list_req.latitude, list_req.longitude, 20000, db)

    if list_req.category is not None:
        query = query.filter(PlaceTable.category_name == list_req.category.value)

    places = query.all()

    for place in places:
        distance = calculate_place_distance(
            list_req.latitude, list_req.longitude, place.latitude, place.longitude)
        place_list_resp.append(PlaceResponse(
            kakao_place_id=place.kakao_place_id,
            kakao_place_url=place.kakao_place_url,
            name=place.name,
            address=place.address_name,
            category=place.category_name,
            distance=distance,
            image_urls=place.image_urls
        ))

    place_list_resp.sort(key=lambda x: x.distance)

    return place_list_resp


def list_places_by_keyword(list_req: PlaceKeywordList, db: Session):
    """
    키워드 기반 장소 검색
    :param list_req:
    :param db:
    :return:
    """
    kakao_places = []
    place_list_resp: List[PlaceResponse] = []

    for page in range(1, 11):
        page_places = get_places_with_keyword(
            params=SearchKeywordParams(
                query=list_req.keyword,
                x=list_req.longitude,
                y=list_req.latitude,
                sort=list_req.sort_by
            ),
            page=page
        )
        kakao_places.extend(page_places.get("documents", []))

    db_places = list_places_in_target_radius(list_req.latitude, list_req.longitude, 20000, db).all()
    db_place_ids = {place.id: place for place in db_places}
    keyword_places = [db_place_ids[place["id"]]
                      for place in kakao_places if place["id"] in db_place_ids]

    for place in keyword_places:
        distance = calculate_place_distance(
            list_req.latitude, list_req.longitude, place.latitude, place.longitude)
        place_list_resp.append(PlaceResponse(
            kakao_place_id=place.kakao_place_id,
            kakao_place_url=place.kakao_place_url,
            name=place.name,
            address=place.address_name,
            category=place.category_name,
            distance=distance,
            image_urls=place.image_urls
        ))

    return place_list_resp


def list_places_in_target_radius(latitude: float, longitude: float, radius: int, db: Session):
    """
    반경 범위 내에 장소 필터링해서 db에서 꺼내오는 함수
    :param latitude:
    :param longitude:
    :param radius:
    :param db:
    :return:
    """
    return db.query(PlaceTable).filter(
        func.acos(
            func.sin(func.radians(latitude))
            * func.sin(func.radians(PlaceTable.latitude)) +
            func.cos(func.radians(latitude))
            * func.cos(func.radians(PlaceTable.latitude))
            * func.cos(func.radians(PlaceTable.longitude) - func.radians(longitude))
        ) * 6371000 <= radius
    )
