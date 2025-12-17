from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_role_service
from app.application.services.role_service import RoleService
from app.domain.schemas import RoleCreate, RoleRead, RoleUpdate

router = APIRouter(prefix="/roles", tags=["roles"])


@router.post("/", response_model=RoleRead, status_code=status.HTTP_201_CREATED)
def create_role(payload: RoleCreate, service: RoleService = Depends(get_role_service)) -> RoleRead:
    return service.create_role(payload)


@router.get("/", response_model=list[RoleRead])
def list_roles(name: str | None = None, service: RoleService = Depends(get_role_service)) -> list[RoleRead]:
    return service.list_roles(name=name)


@router.put("/{role_id}", response_model=RoleRead)
def update_role(
    role_id: int, payload: RoleUpdate, service: RoleService = Depends(get_role_service)
) -> RoleRead:
    updated = service.update_role(role_id, payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
    return updated


@router.delete("/{role_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_role(role_id: int, service: RoleService = Depends(get_role_service)) -> None:
    deleted = service.delete_role(role_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Role not found")
