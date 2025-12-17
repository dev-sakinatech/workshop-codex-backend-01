from typing import List, Optional

from app.domain.schemas import RoleCreate, RoleRead, RoleUpdate
from app.domain.repositories import RoleRepository


class RoleService:
    def __init__(self, repository: RoleRepository):
        self.repository = repository

    def create_role(self, data: RoleCreate) -> RoleRead:
        return RoleRead.model_validate(self.repository.create(data))

    def list_roles(self, name: Optional[str] = None) -> List[RoleRead]:
        roles = self.repository.get_all(name=name)
        return [RoleRead.model_validate(role) for role in roles]

    def update_role(self, role_id: int, data: RoleUpdate) -> Optional[RoleRead]:
        updated = self.repository.update(role_id, data)
        return RoleRead.model_validate(updated) if updated else None

    def delete_role(self, role_id: int) -> bool:
        return self.repository.delete(role_id)
