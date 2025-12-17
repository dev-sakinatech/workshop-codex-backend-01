import os

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

SQLALCHEMY_DATABASE_URL = "sqlite+pysqlite:///:memory:"
os.environ.setdefault("DATABASE_URL", SQLALCHEMY_DATABASE_URL)

from app.core.database import get_db
from app.domain.models import Base
from app.main import app

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


overrides_set = False


@pytest.fixture(autouse=True)
def setup_database():
    global overrides_set
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    if not overrides_set:
        app.dependency_overrides[get_db] = override_get_db
        overrides_set = True
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def client():
    return TestClient(app)


def test_role_crud_flow(client: TestClient):
    create_resp = client.post("/roles/", json={"name": "admin", "description": "Administrator"})
    assert create_resp.status_code == 201
    role_id = create_resp.json()["id"]

    list_resp = client.get("/roles/?name=adm")
    assert list_resp.status_code == 200
    assert any(role["id"] == role_id for role in list_resp.json())

    update_resp = client.put(f"/roles/{role_id}", json={"description": "Updated"})
    assert update_resp.status_code == 200
    assert update_resp.json()["description"] == "Updated"

    delete_resp = client.delete(f"/roles/{role_id}")
    assert delete_resp.status_code == 204


def test_permission_crud_flow(client: TestClient):
    create_resp = client.post("/permissions/", json={"name": "read", "description": "Read access"})
    assert create_resp.status_code == 201
    perm_id = create_resp.json()["id"]

    list_resp = client.get("/permissions/?name=read")
    assert list_resp.status_code == 200
    assert list_resp.json()[0]["id"] == perm_id

    update_resp = client.put(f"/permissions/{perm_id}", json={"description": "Read-only"})
    assert update_resp.status_code == 200
    assert update_resp.json()["description"] == "Read-only"

    delete_resp = client.delete(f"/permissions/{perm_id}")
    assert delete_resp.status_code == 204


def test_user_crud_flow(client: TestClient):
    create_resp = client.post(
        "/users/",
        json={
            "username": "tester",
            "email": "tester@example.com",
            "password_hash": "secretpass",
            "is_active": True,
        },
    )
    assert create_resp.status_code == 201
    user_id = create_resp.json()["id"]

    list_resp = client.get("/users/?username=test")
    assert list_resp.status_code == 200
    assert list_resp.json()[0]["id"] == user_id

    update_resp = client.put(f"/users/{user_id}", json={"is_active": False})
    assert update_resp.status_code == 200
    assert update_resp.json()["is_active"] is False

    delete_resp = client.delete(f"/users/{user_id}")
    assert delete_resp.status_code == 204


def test_role_permission_links(client: TestClient):
    role_id = client.post("/roles/", json={"name": "editor", "description": ""}).json()["id"]
    perm_one = client.post("/permissions/", json={"name": "edit", "description": ""}).json()["id"]
    perm_two = client.post("/permissions/", json={"name": "publish", "description": ""}).json()["id"]

    create_resp = client.post(
        "/role-permissions/", json={"role_id": role_id, "permission_id": perm_one}
    )
    assert create_resp.status_code == 201

    list_resp = client.get(f"/role-permissions/?role_id={role_id}")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    update_resp = client.put(
        f"/role-permissions/{role_id}/{perm_one}", json={"permission_id": perm_two}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["permission_id"] == perm_two

    delete_resp = client.delete(f"/role-permissions/{role_id}/{perm_two}")
    assert delete_resp.status_code == 204


def test_user_role_links(client: TestClient):
    role_id = client.post("/roles/", json={"name": "viewer", "description": ""}).json()["id"]
    user_id = client.post(
        "/users/",
        json={"username": "view", "email": "view@example.com", "password_hash": "secretpass"},
    ).json()["id"]
    new_role_id = client.post("/roles/", json={"name": "auditor", "description": ""}).json()["id"]

    create_resp = client.post(
        "/user-roles/", json={"user_id": user_id, "role_id": role_id}
    )
    assert create_resp.status_code == 201

    list_resp = client.get(f"/user-roles/?user_id={user_id}")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1

    update_resp = client.put(
        f"/user-roles/{user_id}/{role_id}", json={"role_id": new_role_id}
    )
    assert update_resp.status_code == 200
    assert update_resp.json()["role_id"] == new_role_id

    delete_resp = client.delete(f"/user-roles/{user_id}/{new_role_id}")
    assert delete_resp.status_code == 204
