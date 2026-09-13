from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.models.contact import ContactMessage
from app.models.user import User
from app.schemas.contact import ContactCreate, ContactRead

router = APIRouter()


@router.post("", response_model=ContactRead, status_code=status.HTTP_201_CREATED)
def create_contact_message(
    payload: ContactCreate, db: Session = Depends(get_db)
) -> ContactMessage:
    message = ContactMessage(**payload.model_dump())
    db.add(message)
    db.commit()
    db.refresh(message)
    return message


@router.get("/messages", response_model=list[ContactRead])
def list_contact_messages(
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("superadmin", "admin")),
) -> list[ContactMessage]:
    return list(
        db.scalars(select(ContactMessage).order_by(ContactMessage.created_at.desc())).all()
    )
