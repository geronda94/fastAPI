
from auth.manager import get_user_manager, UserManager
from auth.models import User
from auth.schemas import UserRead
from .base_config import current_user, get_redis_strategy, fastapi_users
from fastapi import APIRouter, Depends
from main import redis


router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)



@router.get("/me", response_model=UserRead)
async def read_current_user(user: User = Depends(fastapi_users.current_user())):
    return user




redis_strategy = get_redis_strategy()  
@router.get('/get_tokens')
async def get_tokens():
    token_keys = await redis.keys("fastapi_users_token:*")    
    tokens_info = []
    
    for key in token_keys:

        cleaned_key = key.replace("fastapi_users_token:", "")
        token_data = await redis.get(key)
        
        if token_data:
            try:
                user_id = token_data  # Здесь должна быть ваша логика
                
                tokens_info.append({
                    "token": cleaned_key,  # Используем ключ без префикса
                    "user_id": user_id,
                })
                
            except Exception as e:
                # Если произошла ошибка при декодировании
                tokens_info.append({
                    "token": cleaned_key,  # Используем ключ без префикса
                    "error": str(e)
                })
    
    return tokens_info