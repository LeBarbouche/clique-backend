from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.api.deps import get_db, require_roles
from app.models.news import NewsArticle
from app.models.user import User
from app.schemas.news import NewsCreate, NewsRead

router = APIRouter()


@router.get("", response_model=list[NewsRead])
def list_news(db: Session = Depends(get_db)) -> list[NewsArticle]:
    return list(db.scalars(select(NewsArticle).where(NewsArticle.published.is_(True)).order_by(NewsArticle.created_at.desc())).all())


@router.post("", response_model=NewsRead, status_code=status.HTTP_201_CREATED)
def create_news(payload: NewsCreate, db: Session = Depends(get_db), _: User = Depends(require_roles("superadmin", "admin"))) -> NewsArticle:
    if db.scalar(select(NewsArticle).where(NewsArticle.slug == payload.slug)) is not None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Slug déjà utilisé")
    article = NewsArticle(**payload.model_dump())
    db.add(article)
    db.commit()
    db.refresh(article)
    return article


@router.put("/{article_id}", response_model=NewsRead)
def update_news(article_id: int, payload: NewsCreate, db: Session = Depends(get_db), _: User = Depends(require_roles("superadmin", "admin"))) -> NewsArticle:
    article = db.get(NewsArticle, article_id)
    if article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Actualité introuvable")
    for key, value in payload.model_dump().items():
        setattr(article, key, value)
    db.commit()
    db.refresh(article)
    return article


@router.delete("/{article_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_news(article_id: int, db: Session = Depends(get_db), _: User = Depends(require_roles("superadmin", "admin"))) -> None:
    article = db.get(NewsArticle, article_id)
    if article is not None:
        db.delete(article)
        db.commit()