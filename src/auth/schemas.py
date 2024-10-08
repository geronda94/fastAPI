from typing import Optional
from fastapi_users import schemas
from .models import Roles

class UserRead(schemas.BaseUser[int]):
    id: int
    email: str
    username: str
    role_id: Roles
    is_active: bool = True
    is_superuser: bool = False
    is_verified: bool = False

    class Config:
        from_attributes = True 


class UserCreate(schemas.BaseUserCreate):
    username: str
    email: str
    password: str
    role_id: Roles
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False
    is_verified: Optional[bool] = False
    
    
    
