"""
장소 서비스 로직
"""
from http.client import HTTPException
from typing import List

from app.schemas.place import PlaceResponse, PlaceList, PlaceKeywordList, PlaceListSortType
from app.database.opensearch import list_documents, keyword_to_category, address_keywords
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
                "filter": [
                    {
                        "geo_distance": {
                            "distance": f"{20000}m",
                            "location": {
                                "lat": list_req.latitude,
                                "lon": list_req.longitude
                            }
                        }
                    }
                ]
            }
        },
        "sort": [
            {
                "_score": {
                    "order": "desc"
                }
            }
        ]
    }

    if list_req.category is not None:
        query["query"]["bool"]["must"].append({
            "match": {
                "category": list_req.category.value
            }
        })

    try:
        documents = list_documents("places", query)
        for hit in documents['hits']['hits']:
            place = hit['_source']
            place_id = hit['_id']
            distance = calculate_place_distance(
                list_req.latitude, list_req.longitude,
                place['location']['lat'], place['location']['lon']
            )
            place_list_resp.append(PlaceResponse(
                place_id=place_id,
                name=place["name"],
                address=place["address"],
                road_address=place["road_address"],
                category=place["category"],
                distance=distance,
                image_urls=place.get("image_urls", []),
                phone_number=place.get("phone_number"),
                website_url=place.get("website_url")
            ))

        if list_req.sort_by and list_req.sort_by is PlaceListSortType.SORT_TYPE_DIST:
            place_list_resp.sort(key=lambda x: x.distance)

        return place_list_resp

    except HTTPException as e:
        raise e


def list_places_by_keyword(list_req: PlaceKeywordList) -> List[PlaceResponse]:
    """
    장소 키워드 리스팅 로직
    :param list_req:
    :return:
    """
    place_list_resp: List[PlaceResponse] = []
    category_filter = None
    for kw, category in keyword_to_category.items():
        if kw in list_req.keyword:
            category_filter = category
            break

    address_filter = None
    for addr_kw, address in address_keywords.items():
        if addr_kw in list_req.keyword:
            address_filter = address
            break

    query = {
        "query": {
            "bool": {
                "should": [
                    {
                        "multi_match": {
                            "query": list_req.keyword,
                            "fields": ["name", "address", "road_address"]
                        }
                    }
                ],
                "filter": [
                    {
                        "geo_distance": {
                            "distance": f"{20000}m",
                            "location": {
                                "lat": list_req.latitude,
                                "lon": list_req.longitude
                            }
                        }
                    }
                ]
            }
        },
        "sort": [
            {
                "_score": {  # 점수 기반 정렬
                    "order": "desc"  # 높은 점수부터 정렬
                }
            }
        ]
    }

    if category_filter:
        query['query']['bool']['filter'].append({
            "term": {
                "category": category_filter
            }
        })

    if address_filter:
        query['query']['bool']['filter'].append({
            "wildcard": {
                "address": f"*{address_filter}*"
            }
        })

    try:
        documents = list_documents("places", query)
        for hit in documents['hits']['hits']:
            place = hit['_source']
            place_id = hit['_id']
            distance = calculate_place_distance(
                list_req.latitude, list_req.longitude,
                place['location']['lat'], place['location']['lon']
            )
            place_list_resp.append(PlaceResponse(
                place_id=place_id,
                name=place["name"],
                address=place["address"],
                road_address=place["road_address"],
                category=place["category"],
                distance=distance,
                image_urls=place.get("image_urls", []),
                phone_number=place.get("phone_number"),
                website_url=place.get("website_url")
            ))

        if list_req.sort_by and list_req.sort_by is PlaceListSortType.SORT_TYPE_DIST:
            place_list_resp.sort(key=lambda x: x.distance)

        return place_list_resp

    except HTTPException as e:
        raise e
