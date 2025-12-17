from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.models import Permission
from app.domain.schemas import PermissionCreate, PermissionUpdate
from app.domain.repositories import PermissionRepository


class SQLAlchemyPermissionRepository(PermissionRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: PermissionCreate) -> Permission:
        permission = Permission(name=data.name, description=data.description)
        self.session.add(permission)
        self.session.commit()
        self.session.refresh(permission)
        return permission

    def get_all(self, **filters) -> List[Permission]:
        query = select(Permission)
        if name := filters.get("name"):
            query = query.where(Permission.name.ilike(f"%{name}%"))
        return list(self.session.scalars(query).all())

    def update(self, identifier: int, data: PermissionUpdate) -> Optional[Permission]:
        permission = self.session.get(Permission, identifier)
        if not permission:
            return None
        if data.name is not None:
            permission.name = data.name
        if data.description is not None:
            permission.description = data.description
        self.session.commit()
        self.session.refresh(permission)
        return permission

    def delete(self, identifier: int) -> bool:
        permission = self.session.get(Permission, identifier)
        if not permission:
            return False
        self.session.delete(permission)
        self.session.commit()
        return True
