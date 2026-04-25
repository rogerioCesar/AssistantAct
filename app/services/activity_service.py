from uuid import UUID

from app.models.activity import ActivityCreate, ActivityOut, ActivityUpdate
from app.repositories.activity_repository import ActivityRepository
from app.services.priority_advisor import PriorityAdvisor


class ActivityService:
    """Orquestra regras de negocio para atividades da agenda diaria."""

    def __init__(
        self,
        repository: ActivityRepository | None = None,
        priority_advisor: PriorityAdvisor | None = None,
    ) -> None:
        self._repository = repository or ActivityRepository()
        self._priority_advisor = priority_advisor or PriorityAdvisor()

    def create(self, activity: ActivityCreate) -> ActivityOut:
        priority = activity.priority or self._priority_advisor.suggest(activity)
        activity_with_priority = activity.model_copy(update={"priority": priority})
        return self._repository.create(activity_with_priority)

    def list(self) -> list[ActivityOut]:
        return self._repository.list()

    def get_by_id(self, activity_id: UUID) -> ActivityOut | None:
        return self._repository.get_by_id(activity_id)

    def update(self, activity_id: UUID, activity: ActivityUpdate) -> ActivityOut | None:
        current_activity = self._repository.get_by_id(activity_id)
        if current_activity is None:
            return None

        update_data = activity.model_dump(exclude_unset=True)
        merged_activity = current_activity.model_copy(update=update_data)

        if activity.priority is None:
            update_data["priority"] = self._priority_advisor.suggest(merged_activity)

        activity_with_priority = ActivityUpdate(**update_data)
        return self._repository.update(activity_id, activity_with_priority)

    def delete(self, activity_id: UUID) -> bool:
        return self._repository.delete(activity_id)
