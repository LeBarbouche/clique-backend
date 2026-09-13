from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.models.member import Member
from app.models.user import User
from app.schemas.member import MemberCreate, MemberRead

router = APIRouter()


@router.get("", response_model=list[MemberRead])
def list_members(db: Session = Depends(get_db)) -> list[Member]:
    statement = select(Member).order_by(Member.section, Member.last_name)
    return list(db.scalars(statement).all())


@router.post("", response_model=MemberRead, status_code=status.HTTP_201_CREATED)
def create_member(
    payload: MemberCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("superadmin", "admin")),
) -> Member:
    member = Member(**payload.model_dump())
    db.add(member)
    db.commit()
    db.refresh(member)
    return member


@router.put("/{member_id}", response_model=MemberRead)
def update_member(member_id: int, payload: MemberCreate, db: Session = Depends(get_db), _: User = Depends(require_roles("superadmin", "admin"))) -> Member:
    member = db.get(Member, member_id)
    if member is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Membre introuvable")
    for key, value in payload.model_dump().items():
        setattr(member, key, value)
    db.commit()
    db.refresh(member)
    return member


@router.delete("/{member_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_member(member_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles("superadmin", "admin"))) -> None:
    member = db.get(Member, member_id)
    if member is not None:
        db.delete(member)
        db.commit()
