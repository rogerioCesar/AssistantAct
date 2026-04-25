import asyncio
from collections.abc import Awaitable, Callable
from uuid import uuid4

import httpx
import pytest
from fastapi import FastAPI

from app.api import activity_routes
from app.models.activity import ActivityCreate, ActivityPriority, ActivityUpdate
from app.repositories.activity_repository import ActivityRepository
from app.services.activity_service import ActivityService


class FakePriorityAdvisor:
    def suggest(self, activity: ActivityCreate | ActivityUpdate) -> ActivityPriority:
        return "medium"


@pytest.fixture
def client_factory(monkeypatch: pytest.MonkeyPatch) -> Callable[[], httpx.AsyncClient]:
    isolated_service = ActivityService(
        repository=ActivityRepository(),
        priority_advisor=FakePriorityAdvisor(),
    )
    monkeypatch.setattr(activity_routes, "activity_service", isolated_service)

    app = FastAPI()
    app.include_router(activity_routes.router)
    transport = httpx.ASGITransport(app=app)

    return lambda: httpx.AsyncClient(transport=transport, base_url="http://testserver")


def run_async[T](awaitable: Awaitable[T]) -> T:
    return asyncio.run(awaitable)


def test_create_activity_returns_201(client_factory: Callable[[], httpx.AsyncClient]) -> None:
    async def run_test() -> None:
        async with client_factory() as client:
            response = await client.post("/activities", json={"title": "Saida para terapia"})

        assert response.status_code == 201
        assert response.json()["title"] == "Saida para terapia"
        assert response.json()["priority"] == "medium"

    run_async(run_test())


def test_list_and_get_activity_return_200(client_factory: Callable[[], httpx.AsyncClient]) -> None:
    async def run_test() -> None:
        async with client_factory() as client:
            created_response = await client.post("/activities", json={"title": "Checklist da escola"})
            activity_id = created_response.json()["id"]

            list_response = await client.get("/activities")
            get_response = await client.get(f"/activities/{activity_id}")

        assert list_response.status_code == 200
        assert len(list_response.json()) == 1
        assert get_response.status_code == 200
        assert get_response.json()["id"] == activity_id

    run_async(run_test())


def test_update_activity_returns_200(client_factory: Callable[[], httpx.AsyncClient]) -> None:
    async def run_test() -> None:
        async with client_factory() as client:
            created_response = await client.post("/activities", json={"title": "Organizar mochila"})
            activity_id = created_response.json()["id"]

            response = await client.put(f"/activities/{activity_id}", json={"status": "done"})

        assert response.status_code == 200
        assert response.json()["status"] == "done"

    run_async(run_test())


def test_delete_activity_returns_204(client_factory: Callable[[], httpx.AsyncClient]) -> None:
    async def run_test() -> None:
        async with client_factory() as client:
            created_response = await client.post("/activities", json={"title": "Separar uniforme"})
            activity_id = created_response.json()["id"]

            response = await client.delete(f"/activities/{activity_id}")

        assert response.status_code == 204
        assert response.content == b""

    run_async(run_test())


def test_unknown_activity_id_returns_404(client_factory: Callable[[], httpx.AsyncClient]) -> None:
    async def run_test() -> None:
        unknown_id = uuid4()

        async with client_factory() as client:
            get_response = await client.get(f"/activities/{unknown_id}")
            update_response = await client.put(f"/activities/{unknown_id}", json={"status": "done"})
            delete_response = await client.delete(f"/activities/{unknown_id}")

        assert get_response.status_code == 404
        assert update_response.status_code == 404
        assert delete_response.status_code == 404

    run_async(run_test())
