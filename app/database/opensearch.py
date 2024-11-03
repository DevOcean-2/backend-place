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
