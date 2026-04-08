from urllib.parse import quote


def test_get_activities_returns_activities(client):
    response = client.get("/activities")

    assert response.status_code == 200
    payload = response.json()
    assert "Chess Club" in payload
    assert "Programming Class" in payload


def test_signup_adds_participant(client):
    activity_name = "Chess Club"
    new_email = "tester@mergington.edu"
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup?email={quote(new_email, safe='')}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Signed up {new_email} for {activity_name}"

    refreshed = client.get("/activities").json()
    assert new_email in refreshed[activity_name]["participants"]


def test_signup_duplicate_returns_400(client):
    activity_name = "Chess Club"
    existing_email = "michael@mergington.edu"
    response = client.post(
        f"/activities/{quote(activity_name, safe='')}/signup?email={quote(existing_email, safe='')}"
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_delete_participant_removes_entry(client):
    activity_name = "Programming Class"
    email = "emma@mergington.edu"
    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants?email={quote(email, safe='')}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from {activity_name}"

    refreshed = client.get("/activities").json()
    assert email not in refreshed[activity_name]["participants"]


def test_delete_nonexistent_participant_returns_404(client):
    activity_name = "Gym Class"
    email = "not-a-student@mergington.edu"
    response = client.delete(
        f"/activities/{quote(activity_name, safe='')}/participants?email={quote(email, safe='')}"
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
