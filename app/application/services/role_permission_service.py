from typing import List, Optional

from app.domain.schemas import RolePermissionCreate, RolePermissionRead, RolePermissionUpdate
from app.domain.repositories import RolePermissionRepository


class RolePermissionService:
    def __init__(self, repository: RolePermissionRepository):
        self.repository = repository

    def create_link(self, data: RolePermissionCreate) -> RolePermissionRead:
        created = self.repository.create(data)
        return RolePermissionRead(**created)

    def list_links(
        self, role_id: Optional[int] = None, permission_id: Optional[int] = None
    ) -> List[RolePermissionRead]:
        rows = self.repository.get_all(role_id=role_id, permission_id=permission_id)
        return [RolePermissionRead(**row) for row in rows]

    def update_link(
        self, identifier: tuple, data: RolePermissionUpdate
    ) -> Optional[RolePermissionRead]:
        updated = self.repository.update(identifier, data)
        return RolePermissionRead(**updated) if updated else None

    def delete_link(self, identifier: tuple) -> bool:
        return self.repository.delete(identifier)
