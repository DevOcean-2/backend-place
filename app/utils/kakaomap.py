"""
Kakao Map API
"""
import os
from enum import Enum

import requests

KAKAO_API_KEY = os.getenv('KAKAO_API_KEY')


class SearchResultSortType(Enum):
    """
    장소 키워드 검색 시 정렬 방법
    """
    SORT_TYPE_ACCURACY="accuracy"
    SORT_TYPE_DIST="distance"


class SearchKeywordParams:
    """
    장소 검색 키워드 파라미터
    """
    query: str
    x: str
    y: str
    radius: int = 20000
    sort: SearchResultSortType = SearchResultSortType.SORT_TYPE_ACCURACY


def get_wtm_coordinates(x: float, y: float):
    """
    좌표를 wtm 형식으로 바꾸는 메소드
    :param x:
    :param y:
    :return:
    """
    response = requests.get(
        "https://dapi.kakao.com/v2/local/geo/transcoord.json",
        params={"x": x, "y": y, "output_coord": "WTM"},
        headers={"Authorization": "KakaoAK " + KAKAO_API_KEY},
        timeout=5
    ).json()
    wtm_x, wtm_y = response["documents"][0]["x"], response["documents"][0]["y"]

    return wtm_x, wtm_y


def get_places_with_keyword(params: SearchKeywordParams):
    """
    키워드 기반 장소 리스팅
    :param params:
    :return:
    """
    response = requests.get(
        "https://dapi.kakao.com/v2/local/search/keyword.json",
        params={"query": params.query, "x": params.x,
                "y": params.y, "radius": params.radius, "sort": params.sort},
        headers={"Authorization": "KakaoAK " + KAKAO_API_KEY},
        timeout=5
    ).json()

    return response["documents"]
