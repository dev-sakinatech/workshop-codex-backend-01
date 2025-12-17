from typing import List, Optional

from app.domain.schemas import UserCreate, UserRead, UserUpdate
from app.domain.repositories import UserRepository


class UserService:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def create_user(self, data: UserCreate) -> UserRead:
        return UserRead.model_validate(self.repository.create(data))

    def list_users(self, username: Optional[str] = None, email: Optional[str] = None) -> List[UserRead]:
        users = self.repository.get_all(username=username, email=email)
        return [UserRead.model_validate(user) for user in users]

    def update_user(self, user_id: int, data: UserUpdate) -> Optional[UserRead]:
        updated = self.repository.update(user_id, data)
        return UserRead.model_validate(updated) if updated else None

    def delete_user(self, user_id: int) -> bool:
        return self.repository.delete(user_id)
