from functools import wraps
from typing import Callable, Any
from Log import logger
from Entities.Entity import User
from Repositories.Repository import RoleRepository, UserRepository, UserRoleRepository, RoleResourceRepository


class PermissionDenied(Exception):
    """Custom exception for permission failures"""
    pass

def require_role(*allowed_roles: str):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            current_user: User = getattr(self,'current_user', None)
            if not current_user:
                raise PermissionDenied("Login required")

            # Fetch roles (you can cache this per request)
            user_role_repo = UserRoleRepository(self.db)
            roles = user_role_repo.select({"user_id": current_user.user_id})
            
            user_role_names = set()
            for ur in roles:
                # Assume you have Role entity/repo to get role_name
                role = RoleRepository(self.db).select_by_id(ur.role_id)
                if role:
                    user_role_names.add(role.role_name.lower())

            if not any(r.lower() in user_role_names for r in allowed_roles):
                raise PermissionDenied(f"Required role: {', '.join(allowed_roles)}")

            return func(self, *args, **kwargs)
        return wrapper
    return decorator