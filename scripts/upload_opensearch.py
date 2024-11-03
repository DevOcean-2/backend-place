import requests
import json
from requests_aws4auth import AWS4Auth
import boto3

region = 'ap-northeast-2'
service = 'es'

session = boto3.Session(
    aws_access_key_id="",
    aws_secret_access_key="",
    region_name=region
)
credentials = session.get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)

url = "https://search-balm-opensearch-bmxhjzbqqqcxean7t7oqwv4dwe.ap-northeast-2.es.amazonaws.com/places/_doc"

with open('./scripts/place.json', 'r', encoding='utf-8') as file:
    places_data = json.load(file)

for place in places_data:
    document = {
        "name": place["place_name"],
        "address": place["road_address_name"],
        "category": place["category_name"],
        "location": {
            "lat": float(place["y"]),
            "lon": float(place["x"])
        },
        "image_urls": [],
        "opening_hours": [],
        "phone_number": place["phone"],
        "website_url": place["place_url"]
    }

    response = requests.post(url, json=document, auth=awsauth)

    # 응답 확인
    if response.status_code == 201:
        print("success")
    else:
        print(response.text)
