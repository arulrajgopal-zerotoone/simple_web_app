from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas
from ..database import get_db
from ..deps import get_current_user

router = APIRouter(prefix="/api/records", tags=["records"])


@router.get("/topics", response_model=List[str])
def list_topics(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    rows = (
        db.query(models.UserData.topic)
        .filter(models.UserData.user_id == current_user.user_id)
        .distinct()
        .order_by(models.UserData.topic)
        .all()
    )
    return [row[0] for row in rows]


@router.get("", response_model=List[schemas.RecordOut])
def list_records(current_user: models.User = Depends(get_current_user), db: Session = Depends(get_db)):
    return (
        db.query(models.UserData)
        .filter(models.UserData.user_id == current_user.user_id)
        .order_by(models.UserData.updated_at.desc())
        .all()
    )


@router.get("/by-topic/{topic}", response_model=List[schemas.RecordOut])
def get_by_topic(
    topic: str,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    records = (
        db.query(models.UserData)
        .filter(
            models.UserData.user_id == current_user.user_id,
            models.UserData.topic == topic,
        )
        .all()
    )
    if not records:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No records found for this topic")
    return records


@router.post("", response_model=schemas.RecordOut, status_code=status.HTTP_201_CREATED)
def create_record(
    payload: schemas.RecordCreate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = models.UserData(
        user_id=current_user.user_id,
        topic=payload.topic,
        description=payload.description,
    )
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


def _get_owned_record(record_id: int, current_user: models.User, db: Session) -> models.UserData:
    record = (
        db.query(models.UserData)
        .filter(
            models.UserData.record_id == record_id,
            models.UserData.user_id == current_user.user_id,
        )
        .first()
    )
    if not record:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Record not found")
    return record


@router.put("/{record_id}", response_model=schemas.RecordOut)
def update_record(
    record_id: int,
    payload: schemas.RecordUpdate,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = _get_owned_record(record_id, current_user, db)

    if payload.topic is not None:
        record.topic = payload.topic
    if payload.description is not None:
        record.description = payload.description

    db.commit()
    db.refresh(record)
    return record


@router.delete("/{record_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_record(
    record_id: int,
    current_user: models.User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    record = _get_owned_record(record_id, current_user, db)
    db.delete(record)
    db.commit()
    return None
