from typing import Annotated
from auth.manager import get_user_manager, UserManager
from auth.models import User, Roles
from auth.schemas import UserRead
from .base_config import current_user
from fastapi import APIRouter, Depends, Form,  HTTPException
from main import redis
from .roles import RoleManager,superuser_verify, permission, role, Perms



router = APIRouter(
    prefix='/auth',
    tags=['Auth']
)


async def get_permissions(user: User = Depends(current_user)):
    return RoleManager.get_permissions_by_role_id(user.role_id)


@router.get("/me", response_model=UserRead)
@permission([Perms.CREATE_USERS, Perms.READ_USERS])
async def read_current_user(user: User = Depends(current_user)
                            ):
    return user





@router.get('/get_tokens')
@role([Roles.admin.value])
async def get_tokens(user: User  = Depends(current_user)
                     ):    

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
    

@router.post('/delete_token')
async def delete_token( token_key: Annotated[str, Form(description='Put token here')],
                        superuser: User = Depends(superuser_verify),

                    ):
    
    result = await redis.delete("fastapi_users_token:"+token_key)
    if result:
        return {"message": f"Token {token_key} deleted successfully."}
    else:
        raise HTTPException(status_code=404, detail=f"Token {token_key} not found.")