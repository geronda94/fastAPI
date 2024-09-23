from fastapi_users.authentication import CookieTransport, AuthenticationBackend
from fastapi_users.authentication import JWTStrategy
from base_config import get_redis_strategy

cookie_transport = CookieTransport(cookie_name="bonds", cookie_max_age=3600*24*7)

SECRET = "SECRET"

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(secret=SECRET, lifetime_seconds=3600*24*7)

auth_backend = AuthenticationBackend(
    name="redis",
    transport=cookie_transport,
    get_strategy=get_redis_strategy,
)