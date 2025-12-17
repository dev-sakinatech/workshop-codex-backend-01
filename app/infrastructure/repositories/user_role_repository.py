from datetime import datetime
from typing import List, Optional

from sqlalchemy import and_, select
from sqlalchemy.orm import Session

from app.domain.models import Role, User, user_roles_table
from app.domain.schemas import UserRoleCreate, UserRoleUpdate
from app.domain.repositories import UserRoleRepository


class SQLAlchemyUserRoleRepository(UserRoleRepository):
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: UserRoleCreate) -> dict:
        assigned_at = datetime.utcnow()
        stmt = user_roles_table.insert().values(
            user_id=data.user_id, role_id=data.role_id, assigned_at=assigned_at
        )
        self.session.execute(stmt)
        self.session.commit()
        return {"user_id": data.user_id, "role_id": data.role_id, "assigned_at": assigned_at}

    def get_all(self, **filters) -> List[dict]:
        query = select(user_roles_table)
        if user_id := filters.get("user_id"):
            query = query.where(user_roles_table.c.user_id == user_id)
        if role_id := filters.get("role_id"):
            query = query.where(user_roles_table.c.role_id == role_id)
        result = self.session.execute(query)
        return [dict(row._mapping) for row in result.fetchall()]

    def update(self, identifier: tuple, data: UserRoleUpdate) -> Optional[dict]:
        user_id, role_id = identifier
        query = select(user_roles_table).where(
            and_(user_roles_table.c.user_id == user_id, user_roles_table.c.role_id == role_id)
        )
        current = self.session.execute(query).first()
        if not current:
            return None
        assigned_at = current._mapping.get("assigned_at")
        new_user_id = data.user_id or user_id
        new_role_id = data.role_id or role_id
        self.session.execute(
            user_roles_table.update()
            .where(and_(user_roles_table.c.user_id == user_id, user_roles_table.c.role_id == role_id))
            .values(user_id=new_user_id, role_id=new_role_id)
        )
        self.session.commit()
        return {"user_id": new_user_id, "role_id": new_role_id, "assigned_at": assigned_at}

    def delete(self, identifier: tuple) -> bool:
        user_id, role_id = identifier
        result = self.session.execute(
            user_roles_table.delete().where(
                and_(user_roles_table.c.user_id == user_id, user_roles_table.c.role_id == role_id)
            )
        )
        self.session.commit()
        return result.rowcount > 0

    def list_roles_for_user(self, user_id: int) -> List[Role]:
        user = self.session.get(User, user_id)
        return user.roles if user else []

    def list_users_for_role(self, role_id: int) -> List[User]:
        role = self.session.get(Role, role_id)
        return role.users if role else []
