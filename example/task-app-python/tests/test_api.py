import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_register_and_login():
    # Register a new user
    response = client.post("/auth/register", json={"username": "alice", "password": "password123", "team_id": 1})
    assert response.status_code == 200
    # Login
    response = client.post("/auth/token", data={"username": "alice", "password": "password123"})
    assert response.status_code == 200
    token = response.json()["access_token"]
    assert token

def test_create_task():
    # Register and login
    client.post("/auth/register", json={"username": "bob", "password": "password123", "team_id": 1})
    response = client.post("/auth/token", data={"username": "bob", "password": "password123"})
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    # Create a task
    response = client.post("/tasks/", json={"title": "Test Task", "description": "A test task."}, headers=headers)
    assert response.status_code == 200
    assert response.json()["title"] == "Test Task"

