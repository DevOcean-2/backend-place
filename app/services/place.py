"""
장소 서비스 로직
"""
from http.client import HTTPException
from typing import List

from app.schemas.place import PlaceResponse, PlaceList, PlaceKeywordList
from app.database.opensearch import list_documents
from app.utils.coordinate import calculate_place_distance


def list_places(list_req: PlaceList) -> List[PlaceResponse]:
    """
    장소 리스팅 로직
    :param list_req: 
    :return:
    """
    place_list_resp: List[PlaceResponse] = []
    query = {
        "query": {
            "bool": {
                "must": [],
                "filter": []
            }
        }
    }

    if list_req.category is not None:
        query["query"]["bool"]["must"].append({
            "match": {
                "category": list_req.category.value
            }
        })

    query["query"]["bool"]["filter"].append({
        "geo_distance": {
            "distance": f"{20000}m",
            "location": {
                "lat": list_req.latitude,
                "lon": list_req.longitude
            }
        }
    })

    try:
        documents = list_documents("places", query)
        for hit in documents['hits']['hits']:
            place = hit['_source']
            place_id = hit['_id']
            distance = calculate_place_distance(
                list_req.latitude, list_req.longitude, place['location']['lat'], place['location']['lon']
            )
            place_list_resp.append(PlaceResponse(
                place_id=place_id,
                name=place["name"],
                address=place["address"],
                category=place["category"],
                distance=distance,
                image_urls=place.get("image_urls", []),
                phone_number=place.get("phone_number"),
                website_url=place.get("website_url")
            ))

        place_list_resp.sort(key=lambda x: x.distance)

        return place_list_resp

    except HTTPException as e:
        raise e


# def list_places_by_keyword(list_req: PlaceKeywordList, db: Session):
#     """
#     키워드 기반 장소 검색
#     :param list_req:
#     :param db:
#     :return:
#     """
#     kakao_places = []
#     place_list_resp: List[PlaceResponse] = []
#
#     for page in range(1, 11):
#         page_places = get_places_with_keyword(
#             params=SearchKeywordParams(
#                 query=list_req.keyword,
#                 x=list_req.longitude,
#                 y=list_req.latitude,
#                 sort=list_req.sort_by
#             ),
#             page=page
#         )
#         kakao_places.extend(page_places.get("documents", []))
#
#     db_places = list_places_in_target_radius(list_req.latitude, list_req.longitude, 20000, db).all()
#     db_place_ids = {place.id: place for place in db_places}
#     keyword_places = [db_place_ids[place["id"]]
#                       for place in kakao_places if place["id"] in db_place_ids]
#
#     for place in keyword_places:
#         distance = calculate_place_distance(
#             list_req.latitude, list_req.longitude, place.latitude, place.longitude)
#         place_list_resp.append(PlaceResponse(
#             kakao_place_id=place.kakao_place_id,
#             kakao_place_url=place.kakao_place_url,
#             name=place.name,
#             address=place.address_name,
#             category=place.category_name,
#             distance=distance,
#             image_urls=place.image_urls
#         ))
#
#     return place_list_resp
#
#
# def list_places_in_target_radius(latitude: float, longitude: float, radius: int, db: Session):
#     """
#     반경 범위 내에 장소 필터링해서 db에서 꺼내오는 함수
#     :param latitude:
#     :param longitude:
#     :param radius:
#     :param db:
#     :return:
#     """
#     return db.query(PlaceTable).filter(
#         func.acos(
#             func.sin(func.radians(latitude))
#             * func.sin(func.radians(PlaceTable.latitude)) +
#             func.cos(func.radians(latitude))
#             * func.cos(func.radians(PlaceTable.latitude))
#             * func.cos(func.radians(PlaceTable.longitude) - func.radians(longitude))
#         ) * 6371000 <= radius
#     )
