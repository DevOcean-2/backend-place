import json
import urllib.parse

from fastapi.testclient import TestClient
from app.main import app
from tests.test_setting import my_token, friend_token

client = TestClient(app)


def test_add_favorite_place(my_token):
    response = client.post(
        "http://127.0.0.1:8000/place/favorites",
        json={
            "place_id": "zBt-FZMBRnlUHp69vJqx",
            "favorite_list_name": "즐겨찾기 테스트 리스트"
        },
        headers={"Authorization": f"Bearer {my_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully added a place"}
    test_delete_favorite_place(my_token)


def test_list_favorite_place(my_token):
    response = client.get(
        "https://127.0.0.1:8000/place/favorites",
        params={
            "latitude": 37.40270870047064,
            "longitude": 127.10332989692688,
        },
        headers={"Authorization": f"Bearer {my_token}"}
    )
    # assert response.status_code == 200
    print(json.dumps(response.json(), indent=4, ensure_ascii=False))


def test_delete_favorite_place(my_token):
    response = client.delete(
        "https://127.0.0.1:8000/place/favorites",
        params={
            "place_ids": ["zBt-FZMBRnlUHp69vJqx",],
            "favorite_list_name": "즐겨찾기 테스트 리스트"
        },
        headers={"Authorization": f"Bearer {my_token}"}
    )
    assert response.status_code == 200
    assert response.json() == {"message": "Successfully deleted a place"}
