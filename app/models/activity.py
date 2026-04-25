from datetime import datetime, timezone
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, Field


ActivityStatus = Literal["pending", "in_progress", "done", "canceled"]
ActivityPriority = Literal["low", "medium", "high"]


class ActivityCreate(BaseModel):
    """Dados para criar uma atividade da agenda diaria."""

    id: UUID | None = Field(default=None, description="Identificador opcional da atividade.")
    title: str = Field(
        min_length=3,
        max_length=100,
        description="Titulo da atividade.",
    )
    description: str | None = Field(default=None, description="Descricao opcional da atividade.")
    scheduled_time: datetime | None = Field(default=None, description="Horario previsto da atividade.")
    period: str | None = Field(default=None, description="Periodo previsto da atividade.")
    status: ActivityStatus = Field(default="pending", description="Status atual da atividade.")
    priority: ActivityPriority | None = Field(default=None, description="Prioridade sugerida ou informada.")
    visual_card_ids: list[UUID] = Field(default_factory=list, description="Cartoes visuais associados.")
    checklist_id: UUID | None = Field(default=None, description="Checklist associado.")
    timer_id: UUID | None = Field(default=None, description="Temporizador associado.")
    has_changes: bool = Field(default=False, description="Indica se a atividade possui mudancas.")
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        description="Data e hora de criacao.",
    )
    updated_at: datetime | None = Field(default=None, description="Data e hora da ultima atualizacao.")


class ActivityUpdate(BaseModel):
    """Dados para atualizar uma atividade da agenda diaria."""

    title: str | None = Field(default=None, min_length=3, max_length=100, description="Titulo da atividade.")
    description: str | None = Field(default=None, description="Descricao opcional da atividade.")
    scheduled_time: datetime | None = Field(default=None, description="Horario previsto da atividade.")
    period: str | None = Field(default=None, description="Periodo previsto da atividade.")
    status: ActivityStatus | None = Field(default=None, description="Status atual da atividade.")
    priority: ActivityPriority | None = Field(default=None, description="Prioridade sugerida ou informada.")
    visual_card_ids: list[UUID] | None = Field(default=None, description="Cartoes visuais associados.")
    checklist_id: UUID | None = Field(default=None, description="Checklist associado.")
    timer_id: UUID | None = Field(default=None, description="Temporizador associado.")
    has_changes: bool | None = Field(default=None, description="Indica se a atividade possui mudancas.")
    updated_at: datetime | None = Field(default=None, description="Data e hora da ultima atualizacao.")


class ActivityOut(BaseModel):
    """Dados retornados para uma atividade da agenda diaria."""

    id: UUID = Field(description="Identificador da atividade.")
    title: str = Field(min_length=3, max_length=100, description="Titulo da atividade.")
    description: str | None = Field(default=None, description="Descricao opcional da atividade.")
    scheduled_time: datetime | None = Field(default=None, description="Horario previsto da atividade.")
    period: str | None = Field(default=None, description="Periodo previsto da atividade.")
    status: ActivityStatus = Field(description="Status atual da atividade.")
    priority: ActivityPriority = Field(default="medium", description="Prioridade da atividade.")
    visual_card_ids: list[UUID] = Field(default_factory=list, description="Cartoes visuais associados.")
    checklist_id: UUID | None = Field(default=None, description="Checklist associado.")
    timer_id: UUID | None = Field(default=None, description="Temporizador associado.")
    has_changes: bool = Field(default=False, description="Indica se a atividade possui mudancas.")
    created_at: datetime = Field(description="Data e hora de criacao.")
    updated_at: datetime | None = Field(default=None, description="Data e hora da ultima atualizacao.")
