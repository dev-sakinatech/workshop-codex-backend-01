from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


class RoleBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None


class RoleCreate(RoleBase):
    pass


class RoleUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None


class RoleRead(RoleBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class PermissionBase(BaseModel):
    name: str = Field(..., max_length=100)
    description: Optional[str] = None


class PermissionCreate(PermissionBase):
    pass


class PermissionUpdate(BaseModel):
    name: Optional[str] = Field(default=None, max_length=100)
    description: Optional[str] = None


class PermissionRead(PermissionBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class UserBase(BaseModel):
    username: str = Field(..., max_length=50)
    email: EmailStr
    is_active: Optional[bool] = True


class UserCreate(UserBase):
    password_hash: str = Field(..., min_length=8)


class UserUpdate(BaseModel):
    username: Optional[str] = Field(default=None, max_length=50)
    email: Optional[EmailStr] = None
    password_hash: Optional[str] = Field(default=None, min_length=8)
    is_active: Optional[bool] = None


class UserRead(UserBase):
    id: int
    created_at: datetime
    updated_at: datetime
    password_hash: str

    class Config:
        from_attributes = True


class RolePermissionBase(BaseModel):
    role_id: int
    permission_id: int


class RolePermissionCreate(RolePermissionBase):
    pass


class RolePermissionUpdate(BaseModel):
    role_id: Optional[int] = None
    permission_id: Optional[int] = None


class RolePermissionRead(RolePermissionBase):
    granted_at: datetime

    class Config:
        from_attributes = True


class UserRoleBase(BaseModel):
    user_id: int
    role_id: int


class UserRoleCreate(UserRoleBase):
    pass


class UserRoleUpdate(BaseModel):
    user_id: Optional[int] = None
    role_id: Optional[int] = None


class UserRoleRead(UserRoleBase):
    assigned_at: datetime

    class Config:
        from_attributes = True
