"""
좌표 관련 유틸 함수들
"""
from math import radians, sin, cos, acos


def calculate_place_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> int:
    """
    두 좌표간 거리 계산 (m)
    :param lat1: 
    :param lon1: 
    :param lat2: 
    :param lon2: 
    :return: 
    """
    lat1_rad = radians(lat1)
    lon1_rad = radians(lon1)
    lat2_rad = radians(lat2)
    lon2_rad = radians(lon2)

    distance = acos(
        sin(lat1_rad) * sin(lat2_rad) +
        cos(lat1_rad) * cos(lat2_rad) * cos(lon2_rad - lon1_rad)
    ) * 6371000

    return int(distance)
