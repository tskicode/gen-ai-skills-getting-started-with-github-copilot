import pytest
from fastapi import status

def test_root_redirect(client):
    """Test that root path returns index.html content"""
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    # FastAPI serves the static file directly instead of redirecting

def test_get_activities(client):
    """Test getting activities list"""
    response = client.get("/activities")
    assert response.status_code == status.HTTP_200_OK
    activities = response.json()
    
    # Check structure of activities
    assert isinstance(activities, dict)
    assert len(activities) > 0
    
    # Check first activity has required fields
    first_activity = next(iter(activities.values()))
    assert "description" in first_activity
    assert "schedule" in first_activity
    assert "max_participants" in first_activity
    assert "participants" in first_activity
    assert isinstance(first_activity["participants"], list)

def test_signup_new_participant(client):
    """Test signing up a new participant for an activity"""
    activity_name = "Chess Club"
    email = "new.student@mergington.edu"
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == status.HTTP_200_OK
    result = response.json()
    assert "message" in result
    assert email in result["message"]
    assert activity_name in result["message"]
    
    # Verify participant was added
    activities = client.get("/activities").json()
    assert email in activities[activity_name]["participants"]

def test_signup_existing_participant(client):
    """Test that signing up an existing participant returns an error"""
    activity_name = "Chess Club"
    email = "michael@mergington.edu"  # Already registered in test data
    
    response = client.post(
        f"/activities/{activity_name}/signup",
        params={"email": email}
    )
    
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    result = response.json()
    assert "detail" in result
    assert "already signed up" in result["detail"].lower()

def test_signup_nonexistent_activity(client):
    """Test signing up for a non-existent activity"""
    response = client.post(
        "/activities/NonexistentClub/signup",
        params={"email": "student@mergington.edu"}
    )
    
    assert response.status_code == status.HTTP_404_NOT_FOUND
    result = response.json()
    assert "detail" in result
    assert "not found" in result["detail"].lower()