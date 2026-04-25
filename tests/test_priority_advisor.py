from urllib.error import URLError

from app.models.activity import ActivityCreate
from app.services import priority_advisor as priority_advisor_module
from app.services.priority_advisor import PriorityAdvisor


def test_suggest_returns_high_priority_for_important_activity() -> None:
    advisor = PriorityAdvisor(api_key=None)

    priority = advisor.suggest(ActivityCreate(title="Saida para terapia"))

    assert priority == "high"


def test_suggest_returns_medium_priority_for_routine_activity() -> None:
    advisor = PriorityAdvisor(api_key=None)

    priority = advisor.suggest(ActivityCreate(title="Checklist da escola"))

    assert priority == "medium"


def test_suggest_returns_low_priority_for_simple_activity() -> None:
    advisor = PriorityAdvisor(api_key=None)

    priority = advisor.suggest(ActivityCreate(title="Ler livro"))

    assert priority == "low"


def test_suggest_falls_back_to_local_priority_when_external_call_fails(monkeypatch) -> None:
    def fake_urlopen(*args, **kwargs):
        raise URLError("external service unavailable")

    monkeypatch.setattr(priority_advisor_module, "urlopen", fake_urlopen)
    advisor = PriorityAdvisor(api_key="fake-key", timeout_seconds=0.1)

    priority = advisor.suggest(ActivityCreate(title="Consulta medica"))

    assert priority == "high"
