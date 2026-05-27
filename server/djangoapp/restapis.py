import os

import requests
from dotenv import load_dotenv

load_dotenv()

backend_url = os.getenv('backend_url', default='http://localhost:3030')
sentiment_analyzer_url = os.getenv(
    'sentiment_analyzer_url',
    default='http://localhost:5000/',
)


def get_request(endpoint, **kwargs):
    params = '&'.join([f'{key}={value}' for key, value in kwargs.items()])
    request_url = f'{backend_url}{endpoint}'
    if params:
        request_url = f'{request_url}?{params}'
    response = requests.get(request_url, timeout=10)
    return response.json()


def analyze_review_sentiments(text):
    response = requests.get(f'{sentiment_analyzer_url}analyze/{text}', timeout=10)
    return response.json()


def post_review(data_dict):
    response = requests.post(
        f'{backend_url}/insert_review',
        json=data_dict,
        timeout=10,
    )
    return response.json()
