"""Casos gerados com LLM: docs/testes-integracao-llm.md."""
import json
from uuid import UUID, uuid4
from urllib.error import URLError
from unittest.mock import Mock

import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.api import activity_routes
from app.repositories.activity_repository import ActivityRepository
from app.services.activity_service import ActivityService
from app.services.priority_advisor import PriorityAdvisor


@pytest.fixture
def client(monkeypatch):
    monkeypatch.delenv("OPENAI_API_KEY", raising=False)
    monkeypatch.setenv("OPENAI_BASE_URL", "https://provider.invalid/v1")
    monkeypatch.setattr(activity_routes, "activity_service", ActivityService(
        repository=ActivityRepository(), priority_advisor=PriorityAdvisor()))
    with TestClient(app) as test_client:
        yield test_client


def test_it01_full_lifecycle(client):
    created = client.post("/activities", json={"title": "Consulta de rotina"})
    assert created.status_code == 201
    activity = created.json()
    UUID(activity["id"])
    assert activity["priority"] == "high"
    assert activity["status"] == "pending"
    path = f'/activities/{activity["id"]}'
    assert client.get(path).json() == activity
    assert client.get("/activities").json() == [activity]
    updated = client.put(path, json={"status": "done"})
    assert updated.status_code == 200
    assert updated.json()["status"] == "done"
    assert updated.json()["title"] == activity["title"]
    assert updated.json()["updated_at"] is not None
    assert client.get(path).json() == updated.json()
    deleted = client.delete(path)
    assert deleted.status_code == 204
    assert deleted.content == b""
    assert client.get(path).status_code == 404
    assert client.get("/activities").json() == []


def test_it02_explicit_priority_skips_provider(client, monkeypatch):
    external = Mock(side_effect=AssertionError("Unexpected provider call"))
    monkeypatch.setattr("app.services.priority_advisor.urlopen", external)
    monkeypatch.setattr(activity_routes, "activity_service", ActivityService(
        priority_advisor=PriorityAdvisor(api_key="test-only")))
    response = client.post("/activities", json={"title": "Consulta", "priority": "low"})
    assert response.status_code == 201
    assert response.json()["priority"] == "low"
    external.assert_not_called()


def test_it03_update_recalculates_priority(client):
    created = client.post("/activities", json={"title": "Ler livro"}).json()
    assert created["priority"] == "low"
    path = f'/activities/{created["id"]}'
    response = client.put(path, json={"has_changes": True})
    assert response.status_code == 200
    assert response.json()["priority"] == "high"
    assert client.get(path).json() == response.json()


@pytest.mark.parametrize("payload", [
    {}, {"title": "ab"}, {"title": "x" * 101},
    {"title": "Ler livro", "status": "invalid"},
    {"title": "Ler livro", "priority": "urgent"},
    {"title": "Ler livro", "scheduled_time": "invalid"},
])
def test_it04_invalid_create_does_not_persist(client, payload):
    assert client.post("/activities", json=payload).status_code == 422
    assert client.get("/activities").json() == []


@pytest.mark.parametrize("method", ["get", "put", "delete"])
@pytest.mark.parametrize("identifier,expected", [("invalid", 422), (str(uuid4()), 404)])
def test_it05_identifier_errors(client, method, identifier, expected):
    kwargs = {"json": {"status": "done"}} if method == "put" else {}
    response = getattr(client, method)(f"/activities/{identifier}", **kwargs)
    assert response.status_code == expected
    assert client.get("/activities").json() == []


def test_it06_invalid_update_preserves_state(client):
    original = client.post("/activities", json={"title": "Ler livro"}).json()
    path = f'/activities/{original["id"]}'
    assert client.put(path, json={"status": "invalid"}).status_code == 422
    assert client.get(path).json() == original


@pytest.mark.parametrize("outcome", ["success", "timeout", "network", "invalid"])
def test_it07_it08_provider_integration(client, monkeypatch, outcome):
    monkeypatch.setattr(activity_routes, "activity_service", ActivityService(
        priority_advisor=PriorityAdvisor(api_key="test-only", model="test-model")))
    def provider(request, timeout):
        assert request.full_url == "https://provider.invalid/v1/responses"
        assert request.get_method() == "POST"
        assert timeout == 2.0
        payload = json.loads(request.data)
        assert payload["model"] == "test-model"
        activity_data = json.loads(payload["input"][1]["content"])
        assert activity_data["activity"]["title"] == "Consulta"
        assert activity_data["fallback_priority"] == "high"
        if outcome == "timeout":
            raise TimeoutError("simulated")
        if outcome == "network":
            raise URLError("simulated")
        text = "medium" if outcome == "success" else "urgent"
        response = Mock()
        response.read.return_value = json.dumps({"output": [{"content": [
            {"type": "output_text", "text": text}]}]}).encode()
        response.__enter__ = Mock(return_value=response)
        response.__exit__ = Mock(return_value=False)
        return response
    external = Mock(side_effect=provider)
    monkeypatch.setattr("app.services.priority_advisor.urlopen", external)
    response = client.post("/activities", json={"title": "Consulta"})
    assert response.status_code == 201
    assert response.json()["priority"] == ("medium" if outcome == "success" else "high")
    path = f'/activities/{response.json()["id"]}'
    assert client.get(path).json() == response.json()
    external.assert_called_once()
