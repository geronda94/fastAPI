from functools import wraps
from .base_config import current_user
from .models import RolesEnum
from fastapi import Depends, HTTPException
from auth.models import User


def superuser_verify(user: User = Depends(current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="No permission!")
    return user




class BasePermissions:
    read = False
    update = False
    create = False
    delete = False
    read_users = False
    update_users = False
    create_users = False
    delete_users = False

    class CheckPermissions:
        def __init__(self, permissions):
            self.permissions = permissions

        def __getattr__(self, permission_name: str):
            """Проверяет право доступа через точку (например, check.read_users)"""
            if not getattr(self.permissions, permission_name, False):
                raise HTTPException(status_code=403, detail=f"Permission denied: {permission_name}")
            return True  

    @property
    def check(self):
        """Возвращает экземпляр CheckPermissions для проверки через точку"""
        return self.CheckPermissions(self)

        

class Admin(BasePermissions):
    read = True
    update = True
    create = True
    delete = True
    read_users = True
    update_users = True
    create_users = True
    delete_users = True
    confirm_users = True

class Moderator(BasePermissions):
    read = True
    create = True
    update = True
    read_users = True
    
class User(BasePermissions):
    read = True
    read_users = True

class Guest(BasePermissions):
    read = True









class RoleManager:
    roles_mapping = {
        RolesEnum.admin.value: Admin,
        RolesEnum.moderator.value: Moderator,
        RolesEnum.user.value: User,
        RolesEnum.guest.value: Guest,
    }

    @staticmethod
    def get_permissions_by_role_id(role_id: int) -> BasePermissions:
        role_class = RoleManager.roles_mapping.get(role_id)
        if role_class:
            return role_class()
        raise HTTPException(status_code=404, detail="No permission!")
    
    @staticmethod
    def get_permissions_by_role(role: RolesEnum) -> BasePermissions:
        role_class = RoleManager.roles_mapping.get(role)
        if role_class:
            return role_class()
        raise HTTPException(status_code=404, detail="Role not found.")
    
    
# Декоратор для проверки ролей пользователя
def role(allowed_roles: list[RolesEnum]):
    """_summary_

    Args:
        allowed_roles [(RolesEnum.admin.value, RolesEnum.moderator.value, RolesEnum.user.value, RolesEnum.guest.value)]: _description_
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user: User = Depends(current_user), **kwargs):
            # Проверяем роль пользователя напрямую через user.role_id
            if RolesEnum(user.role_id) not in allowed_roles:
                raise HTTPException(status_code=403, detail="You do not have the required role!")
            return await func(*args, user=user, **kwargs)
        return wrapper
    return decorator

    
def permission(permission_name: str):
    """_summary_

    Args:
        permission_name ('read'): _description_
        permission_name ('update'): _description_
        permission_name ('create'): _description_
        permission_name ('delete'): _description_
        permission_name ('read_users'): _description_
        permission_name ('read_users'): _description_
        permission_name ('update_users'): _description_
        permission_name ('create_users'): _description_
        permission_name ('delete_users'): _description_
        permission_name ('confirm_users'): _description_           
    
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user: User = Depends(current_user), **kwargs):
            permissions = RoleManager.get_permissions_by_role_id(user.role_id)
            if not getattr(permissions.check, permission_name, False):
                raise HTTPException(status_code=403, detail=f"Permission '{permission_name}' denied!")

            return await func(user, *args, **kwargs)  # Обратите внимание на это место
        return wrapper
    return decorator
