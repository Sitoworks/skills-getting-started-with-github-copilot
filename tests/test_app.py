import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


def test_get_activities():
    # Arrange: No special setup needed as activities are in-memory

    # Act: Make GET request to /activities
    response = client.get("/activities")

    # Assert: Check status code and response content
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    assert "Programming Class" in data


def test_signup_success():
    # Arrange: Choose an activity and a new email
    activity_name = "Basketball Team"
    email = "newstudent@mergington.edu"

    # Act: Make POST request to signup
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check success response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Signed up {email} for {activity_name}" in data["message"]


def test_signup_duplicate():
    # Arrange: Sign up a student first
    activity_name = "Soccer Club"
    email = "test@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act: Try to sign up the same student again
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check error response
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student already signed up" in data["detail"]


def test_signup_invalid_activity():
    # Arrange: Use a non-existent activity
    activity_name = "NonExistent Activity"
    email = "student@mergington.edu"

    # Act: Make POST request
    response = client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Assert: Check 404 response
    assert response.status_code == 404
    data = response.json()
    assert "detail" in data
    assert "Activity not found" in data["detail"]


def test_unregister_success():
    # Arrange: Sign up a student first
    activity_name = "Art Club"
    email = "removeme@mergington.edu"
    client.post(f"/activities/{activity_name}/signup", params={"email": email})

    # Act: Unregister the student
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: Check success response
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert f"Removed {email} from {activity_name}" in data["message"]


def test_unregister_not_signed_up():
    # Arrange: Choose an activity and an email not signed up
    activity_name = "Drama Club"
    email = "notsignedup@mergington.edu"

    # Act: Try to unregister
    response = client.delete(f"/activities/{activity_name}/participants", params={"email": email})

    # Assert: Check error response
    assert response.status_code == 400
    data = response.json()
    assert "detail" in data
    assert "Student not signed up for this activity" in data["detail"]