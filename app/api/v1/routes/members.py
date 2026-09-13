from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.member import Member
from app.schemas.member import MemberCreate, MemberRead

router = APIRouter()


@router.get("", response_model=list[MemberRead])
def list_members(db: Session = Depends(get_db)) -> list[Member]:
    statement = select(Member).order_by(Member.section, Member.last_name)
    return list(db.scalars(statement).all())


@router.post("", response_model=MemberRead, status_code=status.HTTP_201_CREATED)
def create_member(payload: MemberCreate, db: Session = Depends(get_db)) -> Member:
    member = Member(**payload.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member
