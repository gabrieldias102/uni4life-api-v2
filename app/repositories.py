from datetime import datetime
from typing import List, Optional

from sqlalchemy import or_, select
from sqlalchemy.orm import Session, joinedload

from app.models import Comment, Connection, Post, Repost, User
from app.schemas import CommentCreate, PostCreate, PostUpdate, UserCreate, UserUpdate


def _normalize_connection_uids(user_uid: str, connected_user_uid: str) -> tuple[str, str]:
    if user_uid <= connected_user_uid:
        return (user_uid, connected_user_uid)
    return (connected_user_uid, user_uid)


class UserRepository:

    def __init__(self, db: Session):
        self._db = db

    def list(self) -> List[User]:
        return list(self._db.scalars(select(User).order_by(User.id)).all())

    def get(self, user_uid: str) -> Optional[User]:
        statement = select(User).where(User.user_uid == user_uid)
        return self._db.scalar(statement)

    def get_by_username(self, username: str) -> Optional[User]:
        statement = select(User).where(User.username == username)
        return self._db.scalar(statement)

    def create(self, payload: UserCreate) -> User:
        now = datetime.utcnow()
        user = User(
            user_uid=payload.user_uid,
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

    def update(self, user_uid: str, payload: UserUpdate) -> Optional[User]:
       
        user = self.get(user_uid)
        if user is None: return None
        if payload.full_name is not None: user.full_name = payload.full_name
        if payload.bio is not None: user.bio = payload.bio
        user.updated_at = datetime.utcnow()
        self._db.commit()
        self._db.refresh(user)
        return user

    def delete(self, user_uid: str) -> bool:
        
        user = self.get(user_uid)
        if user is None: return False
        self._db.delete(user)
        self._db.commit()
        return True


class ConnectionRepository:
 
    def __init__(self, db: Session):
        self._db = db

    def list_by_user(self, user_uid: str) -> List[Connection]:
        statement = (
            select(Connection)
            .where(or_(Connection.user_uid == user_uid, Connection.connected_user_uid == user_uid))
            .options(joinedload(Connection.user), joinedload(Connection.connected_user))
            .order_by(Connection.id)
        )
        return list(self._db.scalars(statement).all())

    def exists(self, user_uid: str, connected_user_uid: str) -> bool:
 
        left_uid, right_uid = _normalize_connection_uids(user_uid, connected_user_uid)
        statement = select(Connection.id).where(
            Connection.user_uid == left_uid,
            Connection.connected_user_uid == right_uid,
        )
        return self._db.scalar(statement) is not None

    def create(self, user_uid: str, connected_user_uid: str) -> Connection:
    
        left_uid, right_uid = _normalize_connection_uids(user_uid, connected_user_uid)
        connection = Connection(
            user_uid=left_uid,
            connected_user_uid=right_uid,
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
        statement = select(Post).options(joinedload(Post.author)).order_by(Post.created_at.desc())
        return list(self._db.scalars(statement).all())

    def get(self, post_id: int) -> Optional[Post]:
        statement = select(Post).where(Post.id == post_id).options(joinedload(Post.author))
        return self._db.scalar(statement)

    
    def create(self, payload: PostCreate) -> Post:
        now = datetime.utcnow()
        post = Post(
            author_uid=payload.author_uid,
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
        if post is None: return None
        if payload.content is not None: post.content = payload.content
        post.updated_at = datetime.utcnow()
        self._db.commit()
        self._db.refresh(post)
        return post

    def delete(self, post_id: int) -> bool:
       
        post = self.get(post_id)
        if post is None: return False
        self._db.delete(post)
        self._db.commit()
        return True

    def list_by_author(self, author_uid: str) -> List[Post]:
        statement = (
            select(Post)
            .where(Post.author_uid == author_uid)
            .options(joinedload(Post.author)) # Agora isso vai funcionar
            .order_by(Post.created_at.desc())
        )
        return list(self._db.scalars(statement).all())


class CommentRepository:
  
    def __init__(self, db: Session):
        self._db = db

    def list_by_post(self, post_id: int) -> List[Comment]:
        statement = (
            select(Comment)
            .where(Comment.post_id == post_id)
            .options(joinedload(Comment.author))
            .order_by(Comment.created_at.asc())
        )
        return list(self._db.scalars(statement).all())

    def create(self, post_id: int, payload: CommentCreate) -> Comment:
    
        comment = Comment(
            post_id=post_id,
            author_uid=payload.author_uid,
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
        statement = (
            select(Repost)
            .where(Repost.post_id == post_id)
            .options(joinedload(Repost.user))
            .order_by(Repost.created_at.desc())
        )
        return list(self._db.scalars(statement).all())

    def create(self, post_id: int, user_uid: str) -> Repost:
       
        repost = Repost(
            post_id=post_id,
            user_uid=user_uid,
            created_at=datetime.utcnow(),
        )
        self._db.add(repost)
        self._db.commit()
        self._db.refresh(repost)
        return repost