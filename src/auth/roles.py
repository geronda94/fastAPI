from enum import Enum
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
        raise HTTPException(status_code=404, detail="no permission!")
    
    
    
    
    
