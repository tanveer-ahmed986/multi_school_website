"""
Role-based permissions system.

(T187 - Implementation)

Defines permission matrix and provides decorators for endpoint protection.
"""
from functools import wraps
from typing import Callable, List
from fastapi import HTTPException, status

from src.models.user import User, UserRole


# Permission matrix: role -> resource -> actions
PERMISSIONS = {
    UserRole.SUPER_ADMIN: {
        'schools': ['create', 'read', 'update', 'delete'],
        'faculty': ['create', 'read', 'update', 'delete'],
        'results': ['create', 'read', 'update', 'delete'],
        'notices': ['create', 'read', 'update', 'delete'],
        'gallery': ['create', 'read', 'update', 'delete'],
        'principal': ['create', 'read', 'update', 'delete'],
        'branding': ['create', 'read', 'update', 'delete'],
    },
    UserRole.SCHOOL_ADMIN: {
        'schools': ['read'],  # Can read their own school info
        'faculty': ['create', 'read', 'update', 'delete'],
        'results': ['create', 'read', 'update', 'delete'],
        'notices': ['create', 'read', 'update', 'delete'],
        'gallery': ['create', 'read', 'update', 'delete'],
        'principal': ['create', 'read', 'update', 'delete'],
        'branding': ['create', 'read', 'update', 'delete'],
    },
    UserRole.STAFF: {
        'schools': [],  # No school management
        'faculty': [],  # Cannot manage faculty
        'results': [],  # Cannot manage results
        'notices': ['create', 'read', 'update', 'delete'],  # Can manage notices
        'gallery': ['create', 'read', 'delete'],  # Can manage gallery
        'principal': [],  # Cannot update principal
        'branding': [],  # Cannot update branding
    },
}


def check_permission(role: UserRole, resource: str, action: str) -> bool:
    """
    Check if a role has permission to perform an action on a resource.

    Args:
        role: User role (SUPER_ADMIN, SCHOOL_ADMIN, STAFF)
        resource: Resource type (faculty, results, notices, gallery, etc.)
        action: Action to perform (create, read, update, delete)

    Returns:
        bool: True if permission granted, False otherwise
    """
    if role not in PERMISSIONS:
        return False

    if resource not in PERMISSIONS[role]:
        return False

    return action in PERMISSIONS[role][resource]


def require_role(*allowed_roles: UserRole):
    """
    Decorator to require specific roles for endpoint access.

    Usage:
        @require_role(UserRole.SCHOOL_ADMIN, UserRole.SUPER_ADMIN)
        def admin_only_endpoint(...):
            pass

    Args:
        *allowed_roles: Variable number of UserRole values that are allowed

    Raises:
        HTTPException: 403 Forbidden if user doesn't have required role
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user: User = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required role: {[r.value for r in allowed_roles]}"
                )

            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            # Extract current_user from kwargs
            current_user: User = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            if current_user.role not in allowed_roles:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. Required role: {[r.value for r in allowed_roles]}"
                )

            return func(*args, **kwargs)

        # Return async wrapper if function is async, else sync wrapper
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator


def require_permission(resource: str, action: str):
    """
    Decorator to require specific permission for endpoint access.

    Usage:
        @require_permission('faculty', 'create')
        def create_faculty_endpoint(...):
            pass

    Args:
        resource: Resource type (faculty, results, notices, etc.)
        action: Action to perform (create, read, update, delete)

    Raises:
        HTTPException: 403 Forbidden if user doesn't have required permission
    """
    def decorator(func: Callable) -> Callable:
        @wraps(func)
        async def async_wrapper(*args, **kwargs):
            current_user: User = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            if not check_permission(current_user.role, resource, action):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. You do not have permission to {action} {resource}."
                )

            return await func(*args, **kwargs)

        @wraps(func)
        def sync_wrapper(*args, **kwargs):
            current_user: User = kwargs.get('current_user')
            if not current_user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Authentication required"
                )

            if not check_permission(current_user.role, resource, action):
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Access denied. You do not have permission to {action} {resource}."
                )

            return func(*args, **kwargs)

        # Return async wrapper if function is async, else sync wrapper
        import asyncio
        if asyncio.iscoroutinefunction(func):
            return async_wrapper
        else:
            return sync_wrapper

    return decorator
