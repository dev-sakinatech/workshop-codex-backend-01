from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.domain.models import Permission, Role, role_permissions_table
from app.domain.schemas import RolePermissionCreate, RolePermissionUpdate
from app.domain.repositories import RolePermissionRepository


class SQLAlchemyRolePermissionRepository(RolePermissionRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: RolePermissionCreate) -> dict:
        granted_at = datetime.utcnow()
        stmt = role_permissions_table.insert().values(
            role_id=data.role_id, permission_id=data.permission_id, granted_at=granted_at
        )
        self.session.execute(stmt)
        self.session.commit()
        return {
            "role_id": data.role_id,
            "permission_id": data.permission_id,
            "granted_at": granted_at,
        }

    def get_all(self, **filters) -> List[dict]:
        query = select(role_permissions_table)
        if role_id := filters.get("role_id"):
            query = query.where(role_permissions_table.c.role_id == role_id)
        if permission_id := filters.get("permission_id"):
            query = query.where(role_permissions_table.c.permission_id == permission_id)
        result = self.session.execute(query)
        return [dict(row._mapping) for row in result.fetchall()]

    def update(self, identifier: tuple, data: RolePermissionUpdate) -> Optional[dict]:
        role_id, permission_id = identifier
        query = select(role_permissions_table).where(
            and_(
                role_permissions_table.c.role_id == role_id,
                role_permissions_table.c.permission_id == permission_id,
            )
        )
        current = self.session.execute(query).first()
        if not current:
            return None
        granted_at = current._mapping.get("granted_at")
        new_role_id = data.role_id or role_id
        new_permission_id = data.permission_id or permission_id
        self.session.execute(
            role_permissions_table.update()
            .where(
                and_(
                    role_permissions_table.c.role_id == role_id,
                    role_permissions_table.c.permission_id == permission_id,
                )
            )
            .values(role_id=new_role_id, permission_id=new_permission_id)
        )
        self.session.commit()
        return {
            "role_id": new_role_id,
            "permission_id": new_permission_id,
            "granted_at": granted_at,
        }

    def delete(self, identifier: tuple) -> bool:
        role_id, permission_id = identifier
        result = self.session.execute(
            role_permissions_table.delete().where(
                and_(
                    role_permissions_table.c.role_id == role_id,
                    role_permissions_table.c.permission_id == permission_id,
                )
            )
        )
        self.session.commit()
        return result.rowcount > 0

    def list_permissions_for_role(self, role_id: int) -> List[Permission]:
        role = self.session.get(Role, role_id)
        return role.permissions if role else []

    def list_roles_for_permission(self, permission_id: int) -> List[Role]:
        permission = self.session.get(Permission, permission_id)
        return permission.roles if permission else []
