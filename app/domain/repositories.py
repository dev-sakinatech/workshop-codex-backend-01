from abc import ABC, abstractmethod
from typing import Generic, List, Optional, TypeVar

from app.domain.models import Permission, Role, User
from app.domain.schemas import (
    PermissionCreate,
    PermissionUpdate,
    RoleCreate,
    RolePermissionCreate,
    RolePermissionUpdate,
    RoleUpdate,
    UserCreate,
    UserRoleCreate,
    UserRoleUpdate,
    UserUpdate,
)

ModelType = TypeVar("ModelType")
CreateSchema = TypeVar("CreateSchema")
UpdateSchema = TypeVar("UpdateSchema")


class RepositoryProtocol(ABC, Generic[ModelType, CreateSchema, UpdateSchema]):
    @abstractmethod
    def create(self, data: CreateSchema) -> ModelType: ...

    @abstractmethod
    def get_all(self, **filters) -> List[ModelType]: ...

    @abstractmethod
    def update(self, identifier, data: UpdateSchema) -> Optional[ModelType]: ...

    @abstractmethod
    def delete(self, identifier) -> bool: ...


class RoleRepository(RepositoryProtocol[Role, RoleCreate, RoleUpdate], ABC):
    pass


class PermissionRepository(RepositoryProtocol[Permission, PermissionCreate, PermissionUpdate], ABC):
    pass


class RolePermissionRepository(RepositoryProtocol, ABC):
    pass


class UserRepository(RepositoryProtocol[User, UserCreate, UserUpdate], ABC):
    pass


class UserRoleRepository(RepositoryProtocol, ABC):
    pass
