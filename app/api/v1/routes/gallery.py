from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.models.gallery import GalleryPhoto
from app.models.user import User
from app.schemas.gallery import GalleryCreate, GalleryRead

router = APIRouter()


@router.get("", response_model=list[GalleryRead])
def list_gallery(db: Session = Depends(get_db)) -> list[GalleryPhoto]:
    return list(db.scalars(select(GalleryPhoto).order_by(GalleryPhoto.year.desc())).all())


@router.post("", response_model=GalleryRead, status_code=status.HTTP_201_CREATED)
def create_photo(
    payload: GalleryCreate,
    db: Session = Depends(get_db),
    _: User = Depends(require_roles("superadmin", "admin")),
) -> GalleryPhoto:
    photo = GalleryPhoto(**payload.model_dump())
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo


@router.put("/{photo_id}", response_model=GalleryRead)
def update_photo(photo_id: int, payload: GalleryCreate, db: Session = Depends(get_db), _: User = Depends(require_roles("superadmin", "admin"))) -> GalleryPhoto:
    photo = db.get(GalleryPhoto, photo_id)
    if photo is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Photo introuvable")
    for key, value in payload.model_dump().items():
        setattr(photo, key, value)
    db.commit()
    db.refresh(photo)
    return photo


@router.delete("/{photo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_photo(photo_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles("superadmin", "admin"))) -> None:
    photo = db.get(GalleryPhoto, photo_id)
    if photo is not None:
        db.delete(photo)
        db.commit()
