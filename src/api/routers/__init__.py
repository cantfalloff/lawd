from .auth import auth_r


routers = [auth_r]

__all__ = ['routers', 'auth_r']
