from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import User
from app.domain.schemas import UserCreate, UserUpdate
from app.domain.repositories import UserRepository


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: UserCreate) -> User:
        user = User(
            username=data.username,
            email=data.email,
            password_hash=data.password_hash,
            is_active=data.is_active,
        )
        self.session.add(user)
        self.session.commit()
        self.session.refresh(user)
        return user

    def get_all(self, **filters) -> List[User]:
        query = select(User)
        if username := filters.get("username"):
            query = query.where(User.username.ilike(f"%{username}%"))
        if email := filters.get("email"):
            query = query.where(User.email.ilike(f"%{email}%"))
        return list(self.session.scalars(query).all())

    def update(self, identifier: int, data: UserUpdate) -> Optional[User]:
        user = self.session.get(User, identifier)
        if not user:
            return None
        if data.username is not None:
            user.username = data.username
        if data.email is not None:
            user.email = data.email
        if data.password_hash is not None:
            user.password_hash = data.password_hash
        if data.is_active is not None:
            user.is_active = data.is_active
        self.session.commit()
        self.session.refresh(user)
        return user

    def delete(self, identifier: int) -> bool:
        user = self.session.get(User, identifier)
        if not user:
            return False
        self.session.delete(user)
        self.session.commit()
        return True
