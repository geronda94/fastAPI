from functools import wraps
from .base_config import current_user
from .models import Roles
from fastapi import Depends, HTTPException
from auth.models import User
from enum import Enum


def superuser_verify(user: User = Depends(current_user)):
    if not user.is_superuser:
        raise HTTPException(status_code=403, detail="No permission!")
    return user


class Perms(Enum):
    READ = "read"
    UPDATE = "update"
    CREATE = "create"
    DELETE = "delete"
    READ_USERS = "read_users"
    UPDATE_USERS = "update_users"
    CREATE_USERS = "create_users"
    DELETE_USERS = "delete_users"
    CONFIRM_USERS = "confirm_users"


class BasePermissions:
    permissions = set()  # Используем множество для хранения разрешений

    class CheckPermissions:
        def __init__(self, permissions):
            self.permissions = permissions

        def has_permissions(self, required_permissions: list[Perms]):
            """Проверяет, есть ли у пользователя все требуемые разрешения"""
            missing_permissions = [perm for perm in required_permissions if perm not in self.permissions]
            if missing_permissions:
                missing_str = ', '.join([perm.value for perm in missing_permissions])
                raise HTTPException(status_code=403, detail=f"Permission(s) denied: {missing_str}")
            return True

    @property
    def check(self):
        """Возвращает экземпляр CheckPermissions для проверки через метод"""
        return self.CheckPermissions(self.permissions)


class Admin(BasePermissions):
    permissions = {
        Perms.READ, 
        Perms.UPDATE, 
        Perms.CREATE, 
        Perms.DELETE,
        Perms.READ_USERS,
        Perms.UPDATE_USERS,
        Perms.CREATE_USERS,
        Perms.DELETE_USERS,
        Perms.CONFIRM_USERS,
    }

class Moderator(BasePermissions):
    permissions = {
        Perms.READ, 
        Perms.CREATE, 
        Perms.UPDATE,
        Perms.READ_USERS,
    }

class User(BasePermissions):
    permissions = {
        Perms.READ, 
        Perms.READ_USERS,
    }

class Guest(BasePermissions):
    permissions = {
        Perms.READ,
    }


class RoleManager:
    roles_mapping = {
        Roles.admin: Admin,
        Roles.moderator: Moderator,
        Roles.user: User,
        Roles.guest: Guest,
    }

    @staticmethod
    def get_permissions_by_role_id(role_id: int) -> BasePermissions:
        role_class = RoleManager.roles_mapping.get(Roles(role_id))
        if role_class:
            return role_class()
        raise HTTPException(status_code=404, detail="No permission!")
    
    @staticmethod
    def get_permissions_by_role(role: Roles) -> BasePermissions:
        role_class = RoleManager.roles_mapping.get(role)
        if role_class:
            return role_class()
        raise HTTPException(status_code=404, detail="Role not found.")


def role(allowed_roles: list[Roles]):
    """
    Декоратор для проверки роли пользователя.
    Args:
        allowed_roles (list[Roles]): Список разрешенных ролей.
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user: User = Depends(current_user), **kwargs):
            # Проверяем роль пользователя через user.role_id
            if Roles(user.role_id) not in allowed_roles:
                raise HTTPException(status_code=403, detail="You do not have the required role!")
            return await func(*args, user=user, **kwargs)
        return wrapper
    return decorator


def permission(required_permissions: list[Perms]):
    """Декоратор для проверки нескольких разрешений"""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, user: User = Depends(current_user), **kwargs):
            permissions = RoleManager.get_permissions_by_role_id(user.role_id)
            if not permissions.check.has_permissions(required_permissions):
                raise HTTPException(status_code=403, detail="Permission denied!")
            return await func(*args, user=user, **kwargs)
        return wrapper
    return decorator
