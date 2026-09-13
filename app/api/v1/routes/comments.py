from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_current_user, get_db, require_roles
from app.models.comment import Comment
from app.models.event import Event
from app.models.gallery import GalleryPhoto
from app.models.news import NewsArticle
from app.models.user import User
from app.schemas.comment import CommentCreate, CommentRead

router = APIRouter()

CONTENT_MODELS = {
    "news": NewsArticle,
    "photo": GalleryPhoto,
    "event": Event,
}


@router.get("/{content_type}/{content_id}", response_model=list[CommentRead])
def list_comments(content_type: str, content_id: int, db: Session = Depends(get_db)) -> list[Comment]:
    return list(db.scalars(select(Comment).where(Comment.content_type == content_type, Comment.content_id == content_id).order_by(Comment.created_at)).all())


@router.post("", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(payload: CommentCreate, db: Session = Depends(get_db), user: User = Depends(get_current_user)) -> Comment:
    content_model = CONTENT_MODELS[payload.content_type]
    if db.scalar(select(content_model.id).where(content_model.id == payload.content_id)) is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Ressource commentée introuvable")
    comment = Comment(**payload.model_dump(), author_id=user.id)
    db.add(comment)
    db.commit()
    db.refresh(comment)
    return comment


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_comment(comment_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles("superadmin", "admin"))) -> None:
    comment = db.get(Comment, comment_id)
    if comment is not None:
        db.delete(comment)
        db.commit()