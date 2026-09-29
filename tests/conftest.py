import copy
import importlib

import pytest
from fastapi.testclient import TestClient


app_module = importlib.import_module("src.app")
initial_activities = copy.deepcopy(app_module.activities)


@pytest.fixture(autouse=True)
def isolate_activities(monkeypatch):
    monkeypatch.setattr(app_module, "activities", copy.deepcopy(initial_activities))


@pytest.fixture
def client():
    with TestClient(app_module.app) as test_client:
        yield test_client
