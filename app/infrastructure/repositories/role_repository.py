from typing import List, Optional

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from app.domain.models import Permission, Role, role_permissions_table
from app.domain.schemas import RoleCreate, RoleUpdate
from app.domain.repositories import RoleRepository


class SQLAlchemyRoleRepository(RoleRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: RoleCreate) -> Role:
        role = Role(name=data.name, description=data.description)
        self.session.add(role)
        self.session.commit()
        self.session.refresh(role)
        return role

    def get_all(self, **filters) -> List[Role]:
        query = select(Role)
        if name := filters.get("name"):
            query = query.where(Role.name.ilike(f"%{name}%"))
        return list(self.session.scalars(query).all())

    def update(self, identifier: int, data: RoleUpdate) -> Optional[Role]:
        role = self.session.get(Role, identifier)
        if not role:
            return None
        if data.name is not None:
            role.name = data.name
        if data.description is not None:
            role.description = data.description
        self.session.commit()
        self.session.refresh(role)
        return role

    def delete(self, identifier: int) -> bool:
        role = self.session.get(Role, identifier)
        if not role:
            return False
        self.session.delete(role)
        self.session.commit()
        return True

    def add_permission(self, role_id: int, permission_id: int) -> None:
        stmt = role_permissions_table.insert().values(role_id=role_id, permission_id=permission_id)
        try:
            self.session.execute(stmt)
            self.session.commit()
        except IntegrityError:
            self.session.rollback()

    def list_permissions(self, role_id: int) -> List[Permission]:
        role = self.session.get(Role, role_id)
        return role.permissions if role else []
