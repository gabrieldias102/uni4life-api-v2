from datetime import datetime
from typing import List, Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session

from app.models import Comment, Connection, Post, Repost, User
from app.schemas import CommentCreate, PostCreate, PostUpdate, UserCreate, UserUpdate


def _normalize_connection_ids(user_id: int, connected_user_id: int) -> tuple[int, int]:
    return tuple(sorted((user_id, connected_user_id)))


class UserRepository:
    def __init__(self, db: Session):
        self._db = db

    def list(self) -> List[User]:
        return list(self._db.scalars(select(User).order_by(User.id)).all())

    def get(self, user_id: int) -> Optional[User]:
        return self._db.get(User, user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        return self._db.scalar(statement)

    def create(self, payload: UserCreate) -> User:
        now = datetime.utcnow()
        user = User(
            full_name=payload.full_name,
            username=payload.username,
            bio=payload.bio,
            joined_at=now,
            updated_at=now,
        )
        self._db.add(user)
        self._db.commit()
        self._db.refresh(user)
        return user

    def update(self, user_id: int, payload: UserUpdate) -> Optional[User]:
        user = self.get(user_id)
        if user is None:
            return None

        if payload.full_name is not None:
            user.full_name = payload.full_name
        if payload.bio is not None:
            user.bio = payload.bio

        user.updated_at = datetime.utcnow()
        self._db.commit()
        self._db.refresh(user)
        return user

    def delete(self, user_id: int) -> bool:
        user = self.get(user_id)
        if user is None:
            return False

        self._db.delete(user)
        self._db.commit()
        return True


class ConnectionRepository:
    def __init__(self, db: Session):
        self._db = db

    def list_by_user(self, user_id: int) -> List[Connection]:
        statement = select(Connection).where(
            or_(Connection.user_id == user_id, Connection.connected_user_id == user_id)
        ).order_by(Connection.id)
        return list(self._db.scalars(statement).all())

    def exists(self, user_id: int, connected_user_id: int) -> bool:
        left_id, right_id = _normalize_connection_ids(user_id, connected_user_id)
        statement = select(Connection.id).where(
            Connection.user_id == left_id,
            Connection.connected_user_id == right_id,
        )
        return self._db.scalar(statement) is not None

    def create(self, user_id: int, connected_user_id: int) -> Connection:
        left_id, right_id = _normalize_connection_ids(user_id, connected_user_id)
        connection = Connection(
            user_id=left_id,
            connected_user_id=right_id,
            created_at=datetime.utcnow(),
        )
        self._db.add(connection)
        self._db.commit()
        self._db.refresh(connection)
        return connection


class PostRepository:
    def __init__(self, db: Session):
        self._db = db

    def list(self) -> List[Post]:
        return list(self._db.scalars(select(Post).order_by(Post.id)).all())

    def get(self, post_id: int) -> Optional[Post]:
        return self._db.get(Post, post_id)

    def create(self, payload: PostCreate) -> Post:
        now = datetime.utcnow()
        post = Post(
            author_id=payload.author_id,
            content=payload.content,
            created_at=now,
            updated_at=now,
            repost_of=payload.repost_of,
        )
        self._db.add(post)
        self._db.commit()
        self._db.refresh(post)
        return post

    def update(self, post_id: int, payload: PostUpdate) -> Optional[Post]:
        post = self.get(post_id)
        if post is None:
            return None

        if payload.content is not None:
            post.content = payload.content

        post.updated_at = datetime.utcnow()
        self._db.commit()
        self._db.refresh(post)
        return post

    def delete(self, post_id: int) -> bool:
        post = self.get(post_id)
        if post is None:
            return False

        self._db.delete(post)
        self._db.commit()
        return True

    def list_by_author(self, author_id: int) -> List[Post]:
        statement = select(Post).where(Post.author_id == author_id).order_by(Post.id)
        return list(self._db.scalars(statement).all())


class CommentRepository:
    def __init__(self, db: Session):
        self._db = db

    def list_by_post(self, post_id: int) -> List[Comment]:
        statement = select(Comment).where(Comment.post_id == post_id).order_by(Comment.id)
        return list(self._db.scalars(statement).all())

    def create(self, post_id: int, payload: CommentCreate) -> Comment:
        comment = Comment(
            post_id=post_id,
            author_id=payload.author_id,
            content=payload.content,
            created_at=datetime.utcnow(),
        )
        self._db.add(comment)
        self._db.commit()
        self._db.refresh(comment)
        return comment


class RepostRepository:
    def __init__(self, db: Session):
        self._db = db

    def list_by_post(self, post_id: int) -> List[Repost]:
        statement = select(Repost).where(Repost.post_id == post_id).order_by(Repost.id)
        return list(self._db.scalars(statement).all())

    def create(self, post_id: int, user_id: int) -> Repost:
        repost = Repost(
            post_id=post_id,
            user_id=user_id,
            created_at=datetime.utcnow(),
        )
        self._db.add(repost)
        self._db.commit()
        self._db.refresh(repost)
        return repost
