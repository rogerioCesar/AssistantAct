import json
import os
from datetime import datetime, timedelta, timezone
from typing import Any
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

from app.models.activity import ActivityCreate, ActivityOut, ActivityPriority, ActivityUpdate

ActivityLike = ActivityCreate | ActivityUpdate | ActivityOut


class PriorityAdvisor:
    """Sugere prioridade para atividades da agenda diaria."""

    _HIGH_PRIORITY_TERMS = ("terapia", "consulta", "medicamento", "saida", "urgente")
    _MEDIUM_PRIORITY_TERMS = ("escola", "checklist", "rotina", "preparacao")
    _VALID_PRIORITIES: set[ActivityPriority] = {"low", "medium", "high"}

    def __init__(
        self,
        api_key: str | None = None,
        model: str | None = None,
        timeout_seconds: float = 2.0,
    ) -> None:
        self._api_key = api_key or os.getenv("OPENAI_API_KEY")
        self._model = model or os.getenv("OPENAI_PRIORITY_MODEL", "gpt-4.1-mini")
        self._base_url = os.getenv("OPENAI_BASE_URL", "https://api.openai.com/v1").rstrip("/")
        self._timeout_seconds = timeout_seconds

    def suggest(self, activity: ActivityLike) -> ActivityPriority:
        fallback_priority = self._suggest_locally(activity)
        if not self._api_key:
            return fallback_priority

        llm_priority = self._suggest_with_llm(activity, fallback_priority)
        return llm_priority or fallback_priority

    def _suggest_locally(self, activity: ActivityLike) -> ActivityPriority:
        text = self._activity_text(activity)

        if activity.has_changes is True:
            return "high"

        if any(term in text for term in self._HIGH_PRIORITY_TERMS):
            return "high"

        if self._is_scheduled_soon(activity):
            return "high"

        if activity.checklist_id is not None or activity.timer_id is not None:
            return "medium"

        if any(term in text for term in self._MEDIUM_PRIORITY_TERMS):
            return "medium"

        return "low"

    def _suggest_with_llm(
        self,
        activity: ActivityLike,
        fallback_priority: ActivityPriority,
    ) -> ActivityPriority | None:
        try:
            payload = self._build_payload(activity, fallback_priority)
            request = Request(
                url=f"{self._base_url}/responses",
                data=json.dumps(payload).encode("utf-8"),
                headers={
                    "Authorization": f"Bearer {self._api_key}",
                    "Content-Type": "application/json",
                },
                method="POST",
            )

            with urlopen(request, timeout=self._timeout_seconds) as response:
                response_data = json.loads(response.read().decode("utf-8"))

            priority = self._extract_priority(response_data)
            if priority in self._VALID_PRIORITIES:
                return priority
        except (TimeoutError, HTTPError, URLError, OSError, ValueError, json.JSONDecodeError):
            return None

        return None

    def _build_payload(self, activity: ActivityLike, fallback_priority: ActivityPriority) -> dict[str, Any]:
        activity_data = activity.model_dump(mode="json", exclude_none=True)
        return {
            "model": self._model,
            "input": [
                {
                    "role": "system",
                    "content": (
                        "Classifique a prioridade de uma atividade de agenda diaria. "
                        "Responda apenas com uma palavra: low, medium ou high."
                    ),
                },
                {
                    "role": "user",
                    "content": json.dumps(
                        {
                            "activity": activity_data,
                            "fallback_priority": fallback_priority,
                            "rules": {
                                "high": "mudancas, terapia, consulta, medicamento, saida, urgente ou evento proximo",
                                "medium": "escola, checklist, rotina, preparacao, temporizador ou apoio visual relevante",
                                "low": "atividade simples sem risco ou urgencia",
                            },
                        },
                        ensure_ascii=True,
                    ),
                },
            ],
            "max_output_tokens": 8,
        }

    def _extract_priority(self, response_data: dict[str, Any]) -> ActivityPriority | None:
        output_text = response_data.get("output_text")
        if isinstance(output_text, str):
            return self._normalize_priority(output_text)

        for output_item in response_data.get("output", []):
            if not isinstance(output_item, dict):
                continue

            for content_item in output_item.get("content", []):
                if not isinstance(content_item, dict):
                    continue

                text = content_item.get("text")
                if isinstance(text, str):
                    priority = self._normalize_priority(text)
                    if priority is not None:
                        return priority

        return None

    def _normalize_priority(self, value: str) -> ActivityPriority | None:
        priority = value.strip().lower().split()[0]
        if priority in self._VALID_PRIORITIES:
            return priority

        return None

    def _activity_text(self, activity: ActivityLike) -> str:
        title = activity.title or ""
        description = activity.description or ""
        return f"{title} {description}".lower()

    def _is_scheduled_soon(self, activity: ActivityLike) -> bool:
        if activity.scheduled_time is None:
            return False

        scheduled_time = activity.scheduled_time
        if scheduled_time.tzinfo is None:
            scheduled_time = scheduled_time.replace(tzinfo=timezone.utc)

        now = datetime.now(timezone.utc)
        return now <= scheduled_time <= now + timedelta(hours=1)
