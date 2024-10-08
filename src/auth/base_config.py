from fastapi_users import FastAPIUsers
from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy

from auth.manager import get_user_manager
from auth.models import User
from config import SECRET_AUTH
import redis.asyncio
from fastapi_users.authentication import RedisStrategy
from database import redis

cookie_transport = CookieTransport(
                                    cookie_name="bonds", 
                                    cookie_max_age=3600*24*7,
                                    cookie_secure=True,   
                                    cookie_samesite="none")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET_AUTH, lifetime_seconds=3600)


def get_redis_strategy() -> RedisStrategy:
    return RedisStrategy(redis,  lifetime_seconds=3600*24*7)

auth_backend = AuthenticationBackend(
    name="redis",  #jwt
    transport=cookie_transport,
    get_strategy=get_redis_strategy, #get_jwt_strategy
)

fastapi_users = FastAPIUsers[User, int](
    get_user_manager,
    [auth_backend],
)

current_user = fastapi_users.current_user()