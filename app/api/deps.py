from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.infrastructure.repositories.permission_repository import SQLAlchemyPermissionRepository
from app.infrastructure.repositories.role_permission_repository import SQLAlchemyRolePermissionRepository
from app.infrastructure.repositories.role_repository import SQLAlchemyRoleRepository
from app.infrastructure.repositories.user_repository import SQLAlchemyUserRepository
from app.infrastructure.repositories.user_role_repository import SQLAlchemyUserRoleRepository
from app.application.services.role_service import RoleService
from app.application.services.permission_service import PermissionService
from app.application.services.user_service import UserService
from app.application.services.role_permission_service import RolePermissionService
from app.application.services.user_role_service import UserRoleService


def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(SQLAlchemyRoleRepository(db))


def get_permission_service(db: Session = Depends(get_db)) -> PermissionService:
    return PermissionService(SQLAlchemyPermissionRepository(db))


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(SQLAlchemyUserRepository(db))


def get_role_permission_service(db: Session = Depends(get_db)) -> RolePermissionService:
    return RolePermissionService(SQLAlchemyRolePermissionRepository(db))


def get_user_role_service(db: Session = Depends(get_db)) -> UserRoleService:
    return UserRoleService(SQLAlchemyUserRoleRepository(db))
