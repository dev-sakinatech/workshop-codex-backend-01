from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_user_role_service
from app.application.services.user_role_service import UserRoleService
from app.domain.schemas import UserRoleCreate, UserRoleRead, UserRoleUpdate

router = APIRouter(prefix="/user-roles", tags=["user-roles"])


@router.post("/", response_model=UserRoleRead, status_code=status.HTTP_201_CREATED)
def create_user_role(
    payload: UserRoleCreate, service: UserRoleService = Depends(get_user_role_service)
) -> UserRoleRead:
    return service.create_link(payload)


@router.get("/", response_model=list[UserRoleRead])
def list_user_roles(
    user_id: int | None = None,
    role_id: int | None = None,
    service: UserRoleService = Depends(get_user_role_service),
) -> list[UserRoleRead]:
    return service.list_links(user_id=user_id, role_id=role_id)


@router.put("/{user_id}/{role_id}", response_model=UserRoleRead)
def update_user_role(
    user_id: int,
    role_id: int,
    payload: UserRoleUpdate,
    service: UserRoleService = Depends(get_user_role_service),
) -> UserRoleRead:
    updated = service.update_link((user_id, role_id), payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mapping not found")
    return updated


@router.delete("/{user_id}/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user_role(
    user_id: int, role_id: int, service: UserRoleService = Depends(get_user_role_service)
) -> None:
    deleted = service.delete_link((user_id, role_id))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mapping not found")
