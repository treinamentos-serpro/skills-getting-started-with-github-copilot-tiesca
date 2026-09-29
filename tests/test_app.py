import importlib
from concurrent.futures import ThreadPoolExecutor
import time

import pytest


app_module = importlib.import_module("src.app")


def test_root_redirects_to_static_index(client):
    response = client.get("/", follow_redirects=False)

    assert response.status_code == 307
    assert response.headers["location"] == "/static/index.html"


def test_get_activities_returns_activity_data(client):
    response = client.get("/activities")

    assert response.status_code == 200
    activities = response.json()
    assert "Chess Club" in activities
    assert activities["Chess Club"]["participants"] == [
        "michael@mergington.edu",
        "daniel@mergington.edu",
    ]


def test_signup_adds_participant(client):
    response = client.post(
        "/activities/Art Club/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 200
    assert "student@example.com" in client.get("/activities").json()["Art Club"]["participants"]


def test_signup_rejects_unknown_activity(client):
    response = client.post(
        "/activities/Unknown Club/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_signup_rejects_duplicate_participant(client):
    response = client.post(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"


def test_signup_rejects_full_activity(client):
    activity = app_module.activities["Art Club"]
    activity["participants"] = [
        f"student-{number}@example.com"
        for number in range(activity["max_participants"])
    ]

    response = client.post(
        "/activities/Art Club/signup",
        params={"email": "last-student@example.com"},
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Activity is full"
    assert "last-student@example.com" not in activity["participants"]


def test_signup_serializes_capacity_check_and_insert():
    activity = app_module.activities["Art Club"]
    activity["participants"] = []
    activity["max_participants"] = 1

    app_module.signup_lock.acquire()
    executor = ThreadPoolExecutor(max_workers=1)
    try:
        signup = executor.submit(
            app_module.signup_for_activity,
            "Art Club",
            "student@example.com",
        )
        time.sleep(0.05)
        assert not signup.done()
        activity["participants"].append("existing@example.com")
    finally:
        app_module.signup_lock.release()
        executor.shutdown()

    with pytest.raises(app_module.HTTPException) as error:
        signup.result()

    assert error.value.status_code == 400
    assert error.value.detail == "Activity is full"


def test_cancel_signup_removes_participant(client):
    response = client.delete(
        "/activities/Chess Club/signup",
        params={"email": "michael@mergington.edu"},
    )

    assert response.status_code == 200
    assert "michael@mergington.edu" not in client.get("/activities").json()["Chess Club"]["participants"]


def test_cancel_signup_rejects_unknown_activity(client):
    response = client.delete(
        "/activities/Unknown Club/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"


def test_cancel_signup_rejects_unregistered_participant(client):
    response = client.delete(
        "/activities/Art Club/signup",
        params={"email": "student@example.com"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Student is not signed up for this activity"