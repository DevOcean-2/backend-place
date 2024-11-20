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

with open('./culture_copy.json', 'r', encoding='utf-8') as file:
    places_data = json.load(file)

for place in places_data:
    document = {
        "name": place["place_name"],
        "road_address": place["road_address_name"],
        "address": place["address_name"],
        "category": "culture",
        "location": {
            "lat": float(place["y"]),
            "lon": float(place["x"])
        },
        "image_urls": place["image_urls"],
        "opening_hours": place["opening_hours"],
        "phone_number": place["phone"],
        "website_url": place["place_url"]
    }

    doc_id = place["place_url"].split("/")[-1]
    
    put_url = f"{url}/{doc_id}"
    response = requests.put(put_url, json=document, auth=awsauth)

    if response.status_code in [200, 201]:
        print(f"Updated document {doc_id}")
    else:
        print(f"Error updating document {doc_id}: {response.text}")
