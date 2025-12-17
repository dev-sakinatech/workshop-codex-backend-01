from fastapi import APIRouter, Depends, HTTPException, status

from app.api.deps import get_user_service
from app.application.services.user_service import UserService
from app.domain.schemas import UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, service: UserService = Depends(get_user_service)) -> UserRead:
    return service.create_user(payload)


@router.get("/", response_model=list[UserRead])
def list_users(
    username: str | None = None,
    email: str | None = None,
    service: UserService = Depends(get_user_service),
) -> list[UserRead]:
    return service.list_users(username=username, email=email)


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    user_id: int, payload: UserUpdate, service: UserService = Depends(get_user_service)
) -> UserRead:
    updated = service.update_user(user_id, payload)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return updated


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int, service: UserService = Depends(get_user_service)) -> None:
    deleted = service.delete_user(user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
