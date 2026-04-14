from datetime import datetime
from typing import Dict, List, Optional

from app.models import Comment, Connection, Post, Repost, User
from app.schemas import CommentCreate, PostCreate, PostUpdate, UserCreate, UserUpdate


class UserRepository:
    def __init__(self):
        self._users: Dict[int, User] = {}
        self._sequence: int = 0

    def list(self) -> List[User]:
        return list(self._users.values())

    def get(self, user_id: int) -> Optional[User]:
        return self._users.get(user_id)

    def get_by_username(self, username: str) -> Optional[User]:
        return next((user for user in self._users.values() if user.username == username), None)

    def create(self, payload: UserCreate) -> User:
        self._sequence += 1
        now = datetime.utcnow()
        user = User(
            id=self._sequence,
            full_name=payload.full_name,
            username=payload.username,
            bio=payload.bio,
            joined_at=now,
            updated_at=now,
        )
        self._users[user.id] = user
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
        self._users[user.id] = user
        return user

    def delete(self, user_id: int) -> bool:
        return self._users.pop(user_id, None) is not None


class ConnectionRepository:
    def __init__(self):
        self._connections: Dict[int, Connection] = {}
        self._sequence: int = 0

    def list_by_user(self, user_id: int) -> List[Connection]:
        return [
            connection
            for connection in self._connections.values()
            if connection.user_id == user_id or connection.connected_user_id == user_id
        ]

    def exists(self, user_id: int, connected_user_id: int) -> bool:
        return any(
            connection.user_id == user_id and connection.connected_user_id == connected_user_id
            or connection.user_id == connected_user_id and connection.connected_user_id == user_id
            for connection in self._connections.values()
        )

    def create(self, user_id: int, connected_user_id: int) -> Connection:
        self._sequence += 1
        connection = Connection(
            id=self._sequence,
            user_id=user_id,
            connected_user_id=connected_user_id,
            created_at=datetime.utcnow(),
        )
        self._connections[connection.id] = connection
        return connection


class PostRepository:
    def __init__(self):
        self._posts: Dict[int, Post] = {}
        self._sequence: int = 0

    def list(self) -> List[Post]:
        return list(self._posts.values())

    def get(self, post_id: int) -> Optional[Post]:
        return self._posts.get(post_id)

    def create(self, payload: PostCreate) -> Post:
        self._sequence += 1
        now = datetime.utcnow()
        post = Post(
            id=self._sequence,
            author_id=payload.author_id,
            content=payload.content,
            created_at=now,
            updated_at=now,
            repost_of=payload.repost_of,
        )
        self._posts[post.id] = post
        return post

    def update(self, post_id: int, payload: PostUpdate) -> Optional[Post]:
        post = self.get(post_id)
        if post is None:
            return None

        if payload.content is not None:
            post.content = payload.content
        post.updated_at = datetime.utcnow()
        self._posts[post.id] = post
        return post

    def delete(self, post_id: int) -> bool:
        return self._posts.pop(post_id, None) is not None

    def list_by_author(self, author_id: int) -> List[Post]:
        return [post for post in self._posts.values() if post.author_id == author_id]


class CommentRepository:
    def __init__(self):
        self._comments: Dict[int, Comment] = {}
        self._sequence: int = 0

    def list_by_post(self, post_id: int) -> List[Comment]:
        return [comment for comment in self._comments.values() if comment.post_id == post_id]

    def create(self, post_id: int, payload: CommentCreate) -> Comment:
        self._sequence += 1
        comment = Comment(
            id=self._sequence,
            post_id=post_id,
            author_id=payload.author_id,
            content=payload.content,
            created_at=datetime.utcnow(),
        )
        self._comments[comment.id] = comment
        return comment


class RepostRepository:
    def __init__(self):
        self._reposts: Dict[int, Repost] = {}
        self._sequence: int = 0

    def list_by_post(self, post_id: int) -> List[Repost]:
        return [repost for repost in self._reposts.values() if repost.post_id == post_id]

    def create(self, post_id: int, user_id: int) -> Repost:
        self._sequence += 1
        repost = Repost(
            id=self._sequence,
            post_id=post_id,
            user_id=user_id,
            created_at=datetime.utcnow(),
        )
        self._reposts[repost.id] = repost
        return repost
