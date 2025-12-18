from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data

def test_signup_and_unregister():
    test_email = "testuser@mergington.edu"
    activity = "Chess Club"
    # Ensure clean state: try to unregister first (ignore result)
    client.post(f"/activities/{activity}/unregister?email={test_email}")
    # Signup
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 200
    # Unregister
    resp2 = client.post(f"/activities/{activity}/unregister?email={test_email}")
    if resp2.status_code != 200:
        print('Unregister failed:', resp2.status_code, resp2.text)
    assert resp2.status_code == 200
    assert resp2.json()["success"] is True

def test_signup_duplicate():
    test_email = "duplicate@mergington.edu"
    activity = "Programming Class"
    # Signup first time
    client.post(f"/activities/{activity}/signup?email={test_email}")
    # Signup again (should fail)
    resp = client.post(f"/activities/{activity}/signup?email={test_email}")
    assert resp.status_code == 400
    assert "already signed up" in resp.json()["detail"]
    # Cleanup
    client.post(f"/activities/{activity}/unregister?email={test_email}")
