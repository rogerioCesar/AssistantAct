from uuid import uuid4

import pytest

from app.models.activity import ActivityCreate, ActivityPriority, ActivityUpdate
from app.repositories.activity_repository import ActivityRepository
from app.services.activity_service import ActivityService


class FakePriorityAdvisor:
    def suggest(self, activity: ActivityCreate | ActivityUpdate) -> ActivityPriority:
        return "medium"


@pytest.fixture
def activity_service() -> ActivityService:
    return ActivityService(
        repository=ActivityRepository(),
        priority_advisor=FakePriorityAdvisor(),
    )


@pytest.fixture
def activity_payload() -> ActivityCreate:
    return ActivityCreate(
        title="Saida para terapia",
        description="Preparar mochila e checklist de saida.",
    )


def test_create_activity_returns_activity_with_generated_id(
    activity_service: ActivityService,
    activity_payload: ActivityCreate,
) -> None:
    activity = activity_service.create(activity_payload)

    assert activity.id is not None
    assert activity.title == activity_payload.title
    assert activity.description == activity_payload.description
    assert activity.status == "pending"
    assert activity.priority == "medium"


def test_list_activities_returns_created_activities(
    activity_service: ActivityService,
    activity_payload: ActivityCreate,
) -> None:
    created_activity = activity_service.create(activity_payload)

    activities = activity_service.list()

    assert activities == [created_activity]


def test_update_activity_changes_existing_activity(
    activity_service: ActivityService,
    activity_payload: ActivityCreate,
) -> None:
    created_activity = activity_service.create(activity_payload)

    updated_activity = activity_service.update(
        created_activity.id,
        ActivityUpdate(title="Terapia finalizada", status="done"),
    )

    assert updated_activity is not None
    assert updated_activity.id == created_activity.id
    assert updated_activity.title == "Terapia finalizada"
    assert updated_activity.status == "done"
    assert updated_activity.updated_at is not None


def test_delete_activity_removes_existing_activity(
    activity_service: ActivityService,
    activity_payload: ActivityCreate,
) -> None:
    created_activity = activity_service.create(activity_payload)

    deleted = activity_service.delete(created_activity.id)

    assert deleted is True
    assert activity_service.get_by_id(created_activity.id) is None
    assert activity_service.list() == []


def test_get_update_and_delete_return_empty_result_for_unknown_id(
    activity_service: ActivityService,
) -> None:
    unknown_id = uuid4()

    assert activity_service.get_by_id(unknown_id) is None
    assert activity_service.update(unknown_id, ActivityUpdate(title="Atividade inexistente")) is None
    assert activity_service.delete(unknown_id) is False
