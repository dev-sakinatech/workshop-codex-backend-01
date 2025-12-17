from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_permission_service
from app.application.services.permission_service import PermissionService
from app.domain.schemas import PermissionCreate, PermissionRead, PermissionUpdate

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.post("/", response_model=PermissionRead, status_code=status.HTTP_201_CREATED)
def create_permission(
    payload: PermissionCreate, service: PermissionService = Depends(get_permission_service)
) -> PermissionRead:
    return service.create_permission(payload)


@router.get("/", response_model=list[PermissionRead])
def list_permissions(
    name: str | None = None, service: PermissionService = Depends(get_permission_service)
) -> list[PermissionRead]:
    return service.list_permissions(name=name)


@router.put("/{permission_id}", response_model=PermissionRead)
def update_permission(
    permission_id: int,
    payload: PermissionUpdate,
    service: PermissionService = Depends(get_permission_service),
) -> PermissionRead:
    updated = service.update_permission(permission_id, payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
    return updated


@router.delete("/{permission_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_permission(
    permission_id: int, service: PermissionService = Depends(get_permission_service)
) -> None:
    deleted = service.delete_permission(permission_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Permission not found")
