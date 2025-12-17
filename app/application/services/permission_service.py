from typing import List, Optional

from app.domain.schemas import PermissionCreate, PermissionRead, PermissionUpdate
from app.domain.repositories import PermissionRepository


class PermissionService:
    def __init__(self, repository: PermissionRepository):
        self.repository = repository

    def create_permission(self, data: PermissionCreate) -> PermissionRead:
        return PermissionRead.model_validate(self.repository.create(data))

    def list_permissions(self, name: Optional[str] = None) -> List[PermissionRead]:
        permissions = self.repository.get_all(name=name)
        return [PermissionRead.model_validate(permission) for permission in permissions]

    def update_permission(self, permission_id: int, data: PermissionUpdate) -> Optional[PermissionRead]:
        updated = self.repository.update(permission_id, data)
        return PermissionRead.model_validate(updated) if updated else None

    def delete_permission(self, permission_id: int) -> bool:
        return self.repository.delete(permission_id)
