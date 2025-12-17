from typing import List, Optional

from app.domain.schemas import UserRoleCreate, UserRoleRead, UserRoleUpdate
from app.domain.repositories import UserRoleRepository


class UserRoleService:
    def __init__(self, repository: UserRoleRepository):
        self.repository = repository

    def create_link(self, data: UserRoleCreate) -> UserRoleRead:
        created = self.repository.create(data)
        return UserRoleRead(**created)

    def list_links(self, user_id: Optional[int] = None, role_id: Optional[int] = None) -> List[UserRoleRead]:
        rows = self.repository.get_all(user_id=user_id, role_id=role_id)
        return [UserRoleRead(**row) for row in rows]

    def update_link(self, identifier: tuple, data: UserRoleUpdate) -> Optional[UserRoleRead]:
        updated = self.repository.update(identifier, data)
        return UserRoleRead(**updated) if updated else None

    def delete_link(self, identifier: tuple) -> bool:
        return self.repository.delete(identifier)
