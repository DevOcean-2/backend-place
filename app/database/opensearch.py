"""
OpenSearch 설정 및 세션 생성
"""
import os
import requests
from requests.exceptions import Timeout, RequestException

from requests_aws4auth import AWS4Auth
import boto3
from dotenv import load_dotenv

load_dotenv()

REGION = "ap-northeast-2"
SERVICE = "es"
DEFAULT_TIMEOUT = 5

session = boto3.Session(
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=REGION
)
credentials = session.get_credentials()
awsauth = AWS4Auth(credentials.access_key,
                   credentials.secret_key, REGION, SERVICE, session_token=credentials.token)

OPENSEARCH_URL = os.getenv("OPENSEARCH_URL")

keyword_to_category = {
    "카페": "cafe",
    "까페": "cafe",
    "커피": "cafe",
    "레스토랑": "restaurant",
    "식당": "restaurant",
    "음식": "restaurant",
    "병원": "hospital",
    "약국": "hospital",
    "진찰": "hospital",
    "호텔": "culture",
    "숙소": "culture",
    "놀이": "culture",
    "공원": "culture"
}

address_keywords = {
    "이매": "분당",
    "판교": "분당",
    "정자": "분당",
    "율동": "분당",
    "서현": "분당",
    "수내": "분당",
    "수정": "성남",
    "중원": "성남",
    "분당": "성남",
    "강남": "강남",
    "선릉": "강남",
    "삼성": "강남",
    "논현": "강남",
    "서초": "서초",
    "양재": "서초",
    "송파": "송파",
    "오금": "송파",
    "가락": "송파",
    "한남": "용산",
    "수지": "용인",
    "반월": "화성",
    "능평": "광주",
}


def create_index(index: str, settings: dict = None):
    """
    인덱스 생성
    """
    url = f"{OPENSEARCH_URL}/{index}"
    headers = {"Content-Type": "application/json"}
    if settings is None:
        settings = {}

    try:
        response = requests.put(url, json=settings, headers=headers,
                                auth=awsauth, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()  # HTTP 에러 발생 시 예외 발생
    except Timeout as e:
        raise Timeout(f"Request timed out after {DEFAULT_TIMEOUT} seconds") from e
    except RequestException as e:
        raise RequestException(f"Error creating index: {e}") from e

    return response.json()


def get_index(index: str):
    """
    인덱스 조회
    """
    url = f"{OPENSEARCH_URL}/{index}"
    try:
        response = requests.get(url, auth=awsauth, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
    except Timeout as e:
        raise Timeout(f"Request timed out after {DEFAULT_TIMEOUT} seconds") from e
    except RequestException as e:
        raise RequestException(f"Error retrieving index: {e}") from e

    return response.json()


def get_document(index: str, doc_id: str):
    """
    document 조회
    """
    url = f"{OPENSEARCH_URL}/{index}/_doc/{doc_id}"
    try:
        response = requests.get(url, auth=awsauth, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
    except Timeout as e:
        raise Timeout(f"Request timed out after {DEFAULT_TIMEOUT} seconds") from e
    except RequestException as e:
        raise RequestException(f"Error retrieving document: {e}") from e

    return response.json()


def list_documents(index: str, query: dict = None):
    """
    document 리스팅
    """
    url = f"{OPENSEARCH_URL}/{index}/_search"
    if query is None:
        try:
            response = requests.get(url, auth=awsauth, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
        except Timeout as e:
            raise Timeout(f"Request timed out after {DEFAULT_TIMEOUT} seconds") from e
        except RequestException as e:
            raise RequestException(f"Error listing documents: {e}") from e
    else:
        try:
            response = requests.post(url, json=query, auth=awsauth, timeout=DEFAULT_TIMEOUT)
            response.raise_for_status()
        except Timeout as e:
            raise Timeout(f"Request timed out after {DEFAULT_TIMEOUT} seconds") from e
        except RequestException as e:
            raise RequestException(f"Error listing documents: {e}") from e

    return response.json()
