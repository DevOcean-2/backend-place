import json
import urllib.parse

from fastapi.testclient import TestClient
from app.main import app
from tests.test_setting import my_token, friend_token

client = TestClient(app)


def test_list_places(my_token):
    response = client.get(
        "http://127.0.0.1:8000/place/places",
        params={
            "latitude": 37.40270870047064,
            "longitude": 127.10332989692688,
            "category": "cafe"
        },
        headers={"Authorization": f"Bearer {my_token}"}
    )
    assert response.status_code == 200
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))


def test_list_places_by_keyword(my_token):
    keyword = "분당_카페"
    encoded_keyword = urllib.parse.quote(keyword)
    response = client.get(
        f"http://127.0.0.1:8000/place/places/search/{encoded_keyword}",
        params={
            "latitude": 37.40270870047064,
            "longitude": 127.10332989692688,
            "sort_by": "distance"
        },
        headers={"Authorization": f"Bearer {my_token}"}
    )
    print(response.json())
    assert response.status_code == 200
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))
