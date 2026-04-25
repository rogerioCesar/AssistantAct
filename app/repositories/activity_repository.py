from datetime import datetime, timezone
from uuid import UUID, uuid4

from app.models.activity import ActivityCreate, ActivityOut, ActivityUpdate


class ActivityRepository:
    """Repositorio em memoria para atividades da agenda diaria."""

    def __init__(self) -> None:
        self._activities: dict[UUID, ActivityOut] = {}

    def create(self, activity: ActivityCreate) -> ActivityOut:
        activity_id = activity.id or uuid4()
        activity_out = ActivityOut(
            **activity.model_dump(exclude={"id"}),
            id=activity_id,
        )
        self._activities[activity_id] = activity_out
        return activity_out

    def list(self) -> list[ActivityOut]:
        return list(self._activities.values())

    def get_by_id(self, activity_id: UUID) -> ActivityOut | None:
        return self._activities.get(activity_id)

    def update(self, activity_id: UUID, activity: ActivityUpdate) -> ActivityOut | None:
        current_activity = self._activities.get(activity_id)
        if current_activity is None:
            return None

        update_data = activity.model_dump(exclude_unset=True)
        update_data["updated_at"] = update_data.get("updated_at") or datetime.now(timezone.utc)

        updated_activity = current_activity.model_copy(update=update_data)
        self._activities[activity_id] = updated_activity
        return updated_activity

    def delete(self, activity_id: UUID) -> bool:
        if activity_id not in self._activities:
            return False

        del self._activities[activity_id]
        return True
