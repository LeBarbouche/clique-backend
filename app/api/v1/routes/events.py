from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.event import Event
from app.schemas.event import EventCreate, EventRead

router = APIRouter()


@router.get("", response_model=list[EventRead])
def list_events(db: Session = Depends(get_db)) -> list[Event]:
    return list(db.scalars(select(Event).order_by(Event.date, Event.start_time)).all())


@router.post("", response_model=EventRead, status_code=status.HTTP_201_CREATED)
def create_event(payload: EventCreate, db: Session = Depends(get_db)) -> Event:
    event = Event(**payload.model_dump())
    db.add(event)
    db.commit()
    db.refresh(event)
    return event
