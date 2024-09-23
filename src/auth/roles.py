from .base_config import current_user
from fastapi import Depends, HTTPException
from auth.models import User


def superuser_verify(user: User = Depends(current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="No permission!")
    return user



from fastapi import HTTPException

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

        

class AdminPermissions(BasePermissions):
    read = True
    update = True
    create = True
    delete = True
    read_users = True
    update_users = True
    create_users = True
    delete_users = True
    confirm_users = True

class ModeratorPermissions(BasePermissions):
    read = True
    create = True
    update = True
    
class UserPermissions(BasePermissions):
    read = True

class GuestPermissions(BasePermissions):
    read = True


class RoleManager:
    roles_mapping = {
        1: AdminPermissions,
        2: ModeratorPermissions,
        3: UserPermissions,
        4: GuestPermissions,
    }

    @staticmethod
    def get_permissions_by_role_id(role_id: int) -> BasePermissions:
        role_class = RoleManager.roles_mapping.get(role_id)
        if role_class:
            return role_class()
        raise HTTPException(status_code=404, detail="no permission!")
    
    
    
    
    
