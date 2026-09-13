from fastapi import APIRouter, Depends, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db
from app.models.gallery import GalleryPhoto
from app.schemas.gallery import GalleryCreate, GalleryRead

router = APIRouter()


@router.get("", response_model=list[GalleryRead])
def list_gallery(db: Session = Depends(get_db)) -> list[GalleryPhoto]:
    return list(db.scalars(select(GalleryPhoto).order_by(GalleryPhoto.year.desc())).all())


@router.post("", response_model=GalleryRead, status_code=status.HTTP_201_CREATED)
def create_photo(
    payload: GalleryCreate, db: Session = Depends(get_db)
) -> GalleryPhoto:
    photo = GalleryPhoto(**payload.model_dump())
    db.add(photo)
    db.commit()
    db.refresh(photo)
    return photo
