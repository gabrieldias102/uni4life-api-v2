from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.repositories import (
    CommentRepository,
    ConnectionRepository,
    PostRepository,
    RepostRepository,
    UserRepository,
)
from app.services import CommentService, PostService, RepostService, UserService


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_user_service(db: Session = Depends(get_db)) -> UserService:
    return UserService(UserRepository(db), ConnectionRepository(db))


def get_post_service(db: Session = Depends(get_db)) -> PostService:
    return PostService(PostRepository(db), UserRepository(db))


def get_comment_service(db: Session = Depends(get_db)) -> CommentService:
    return CommentService(CommentRepository(db), UserRepository(db), PostRepository(db))


def get_repost_service(db: Session = Depends(get_db)) -> RepostService:
    return RepostService(RepostRepository(db), UserRepository(db), PostRepository(db))
