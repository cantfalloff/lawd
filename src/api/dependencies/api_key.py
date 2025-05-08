from fastapi import Request, status

from src.config import API_KEY
from src.common import api_logger


def check_api_key(request: Request):
    headers = request.headers

    if headers.get('x-api-key') != API_KEY:
        api_logger.warning(f'wrong api key. url: {request.url}')

        return {
            'status': status.HTTP_400_BAD_REQUEST,
            'detail': 'wrong api key'
        }
