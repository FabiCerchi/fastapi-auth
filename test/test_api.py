from time import sleep

from fastapi.testclient import TestClient
import sys
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import pytest

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from main import app
from app.db.db import Base
from app.db.db import get_db


db_path = os.path.join(os.path.dirname(__file__), 'test.db')
SQL_ALCHEMY_DATABASE_URL = f'sqlite:///{db_path}'
engine_test = create_engine(SQL_ALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine_test)

def override_get_db():
    db_test  = TestingSessionLocal()
    try:
        yield db_test
    finally:
        db_test.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

USER = {
          "name": "Name Prueba",
          "last_name": "Last Name Prueba",
          "age": 0,
          "email": "prueba@prueba.com",
          "username": "UserPrueba",
          "password": "PasswordPrueba",
          "address": "Address Prueba"
}


@pytest.fixture(scope="session", autouse=True)
def cleanup():
    yield
    # Eliminar el archivo de la base de datos al final de todas las pruebas
    if os.path.exists(db_path):
        os.remove(db_path)
    assert not os.path.exists(db_path)


@pytest.fixture(scope="function", autouse=True)
def setup():
    # Crear las tablas antes de cada prueba
    Base.metadata.create_all(bind=engine_test)
    yield
    # Limpiar las tablas después de cada prueba
    Base.metadata.drop_all(bind=engine_test)


@pytest.fixture
def auth_token():
    client.post("/api/users/", json=USER)  # Crear usuario para login
    response = client.post("/api/auth/login", data={"username": USER['username'], "password": USER['password']})
    return response.json()['access_token']

class TestAuthAPI:
    def test_login(self, auth_token):
        assert auth_token is not None

# Tests Encapsulados en Clases
class TestUserAPI:


    def test_create_user(self):
        response = client.post("/api/users/", json=USER)
        assert response.status_code == 201, f"Error: {response.json()}"
        assert response.json()['username'] == USER['username']

    def test_duplicated_user(self):
        client.post("/api/users/", json=USER)
        response = client.post("/api/users/", json=USER)
        assert response.status_code == 409, f"Error: {response.json()}"

    def test_get_users(self, auth_token):
        response = client.get("/api/users/", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 200, f"Error: {response.json()}"
        assert isinstance(response.json(), list)

    def test_get_user_by_id(self):
        new_user = client.post("/api/users/", json=USER)
        user_id = new_user.json()['id']
        res = client.post("/api/auth/login", data={"username": USER['username'], "password": USER['password']})
        jwt = res.json()['access_token']
        response = client.get(f"/api/users/{user_id}", headers={"Authorization": f"Bearer {jwt}"})
        assert response.status_code == 200, f"Error: {response.json()}"
        assert response.json()['id'] == user_id

    def test_delete_user(self):
        new_user = client.post("/api/users/", json=USER)
        user_id = new_user.json()['id']
        res = client.post("/api/auth/login", data={"username": USER['username'], "password": USER['password']})
        jwt = res.json()['access_token']
        response = client.delete(f"/api/users/{user_id}", headers={"Authorization": f"Bearer {jwt}"})
        assert response.status_code == 200, f"Error: {response.json()}"
        assert response.json()['res'] == "Usuario eliminado"

    def test_update_user(self):
        new_user = client.post("/api/users/", json=USER)
        user_id = new_user.json()['id']
        res = client.post("/api/auth/login", data={"username": USER['username'], "password": USER['password']})
        jwt = res.json()['access_token']
        response = client.patch(f"/api/users/{user_id}", json={"name": "Name Updated"}, headers={"Authorization": f"Bearer {jwt}"})
        assert response.status_code == 200, f"Error: {response.json()}"
        assert response.json()['res'] == "Usuario actualizado"
        response = client.get(f"/api/users/{user_id}", headers={"Authorization": f"Bearer {jwt}"})
        assert response.json()['name'] == "Name Updated"

    def test_auth_no_verify_password(self):
        client.post("/api/users/", json=USER)
        response = client.post("/api/auth/login", data={"username": USER['username'], "password": "PasswordPrueba2"})
        assert response.status_code == 401, f"Error: {response.json()}"

    def test_user_not_found(self, auth_token):
        client.post("/api/auth/login", data={"username": "UserPrueba", "password": "PasswordPrueba"})
        response = client.get(f"/api/users/{2332123}", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404, f"Error: {response.json()}"

    def test_update_duplicated_user(self):
        client.post("/api/users/", json=USER)
        new_user = client.post("/api/users/", json={"name": "Name Prueba 2",
                                                    "last_name": "Last Name Prueba 2",
                                                    "age": 0,
                                                    "email": "prueba2@prueba.com",
                                                    "username": "UserPrueba2",
                                                    "password": "PasswordPrueba2",
                                                    "address": "Address Prueba2"
                                                    })
        user_id = new_user.json()['id']
        res = client.post("/api/auth/login", data={"username": USER['username'], "password": USER['password']})
        jwt = res.json()['access_token']
        response = client.patch(f"/api/users/{user_id}", json={"username": "UserPrueba"}, headers={"Authorization": f"Bearer {jwt}"})
        assert response.status_code == 409, f"Error: {response.json()}"

    def test_update_user_not_found(self, auth_token):
        response = client.patch(f"/api/users/{2332123}", json={"name": "Name Updated"}, headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404, f"Error: {response.json()}"

    def test_delete_user_not_found(self, auth_token):
        response = client.delete(f"/api/users/{2332123}", headers={"Authorization": f"Bearer {auth_token}"})
        assert response.status_code == 404, f"Error: {response.json()}"