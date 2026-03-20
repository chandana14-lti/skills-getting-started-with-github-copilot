"""
Backend FastAPI tests using the AAA (Arrange-Act-Assert) pattern.
"""
import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    # Arrange: (No setup needed for in-memory activities)
    # Act
    response = client.get("/activities")
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_signup_and_prevent_duplicate():
    # Arrange
    activity = "Chess Club"
    email = "student1@mergington.edu"
    # Act
    signup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert signup_resp.status_code == 200
    # Act (try duplicate signup)
    dup_resp = client.post(f"/activities/{activity}/signup?email={email}")
    # Assert
    assert dup_resp.status_code == 400 or dup_resp.status_code == 409

def test_unregister_participant():
    # Arrange
    activity = "Chess Club"
    email = "student2@mergington.edu"
    client.post(f"/activities/{activity}/signup?email={email}")
    # Act
    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert resp.status_code == 200
    # Act (try to unregister again)
    resp2 = client.post(f"/activities/{activity}/unregister?email={email}")
    # Assert
    assert resp2.status_code == 404 or resp2.status_code == 400
