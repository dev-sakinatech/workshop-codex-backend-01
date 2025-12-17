from fastapi import FastAPI

from app.api.routes import permissions, role_permissions, roles, user_roles, users
from app.core.config import get_settings
from app.core.database import engine
from app.domain.models import Base

settings = get_settings()

app = FastAPI(title=settings.app_name, debug=settings.debug)

Base.metadata.create_all(bind=engine)

app.include_router(roles.router)
app.include_router(permissions.router)
app.include_router(users.router)
app.include_router(role_permissions.router)
app.include_router(user_roles.router)


@app.get("/health", tags=["health"])  # simple health endpoint
async def health() -> dict[str, str]:
    return {"status": "ok"}
