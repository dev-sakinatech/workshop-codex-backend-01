from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_role_permission_service
from app.application.services.role_permission_service import RolePermissionService
from app.domain.schemas import RolePermissionCreate, RolePermissionRead, RolePermissionUpdate

router = APIRouter(prefix="/role-permissions", tags=["role-permissions"])


@router.post("/", response_model=RolePermissionRead, status_code=status.HTTP_201_CREATED)
def create_role_permission(
    payload: RolePermissionCreate,
    service: RolePermissionService = Depends(get_role_permission_service),
) -> RolePermissionRead:
    return service.create_link(payload)


@router.get("/", response_model=list[RolePermissionRead])
def list_role_permissions(
    role_id: int | None = None,
    permission_id: int | None = None,
    service: RolePermissionService = Depends(get_role_permission_service),
) -> list[RolePermissionRead]:
    return service.list_links(role_id=role_id, permission_id=permission_id)


@router.put("/{role_id}/{permission_id}", response_model=RolePermissionRead)
def update_role_permission(
    role_id: int,
    permission_id: int,
    payload: RolePermissionUpdate,
    service: RolePermissionService = Depends(get_role_permission_service),
) -> RolePermissionRead:
    updated = service.update_link((role_id, permission_id), payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mapping not found")
    return updated


@router.delete("/{role_id}/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role_permission(
    role_id: int,
    permission_id: int,
    service: RolePermissionService = Depends(get_role_permission_service),
) -> None:
    deleted = service.delete_link((role_id, permission_id))
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Mapping not found")
