from fastapi import Depends

from .api_key import check_api_key


api_key_dp = Depends(check_api_key)

__all__ = ['api_key_dp']
