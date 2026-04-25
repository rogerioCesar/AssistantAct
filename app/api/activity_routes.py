from uuid import UUID

from fastapi import APIRouter, HTTPException, status

from app.models.activity import ActivityCreate, ActivityOut, ActivityUpdate
from app.services.activity_service import ActivityService


router = APIRouter(prefix="/activities", tags=["activities"])
activity_service = ActivityService()


@router.post("", response_model=ActivityOut, status_code=status.HTTP_201_CREATED)
def create_activity(activity: ActivityCreate) -> ActivityOut:
    return activity_service.create(activity)


@router.get("", response_model=list[ActivityOut], status_code=status.HTTP_200_OK)
def list_activities() -> list[ActivityOut]:
    return activity_service.list()


@router.get("/{activity_id}", response_model=ActivityOut, status_code=status.HTTP_200_OK)
def get_activity(activity_id: UUID) -> ActivityOut:
    activity = activity_service.get_by_id(activity_id)
    if activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found.",
        )

    return activity


@router.put("/{activity_id}", response_model=ActivityOut, status_code=status.HTTP_200_OK)
def update_activity(activity_id: UUID, activity: ActivityUpdate) -> ActivityOut:
    updated_activity = activity_service.update(activity_id, activity)
    if updated_activity is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found.",
        )

    return updated_activity


@router.delete("/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(activity_id: UUID) -> None:
    deleted = activity_service.delete(activity_id)
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Activity not found.",
        )
