from typing import List

from app.models import Comment, Connection, Post, Repost, User
from app.repositories import (
    CommentRepository,
    ConnectionRepository,
    PostRepository,
    RepostRepository,
    UserRepository,
)
from app.schemas import (
    CommentCreate,
    PostCreate,
    PostUpdate,
    RepostCreate,
    UserCreate,
    UserUpdate,
)


class UserService:
    def __init__(self, user_repository: UserRepository, connection_repository: ConnectionRepository):
        self._user_repository = user_repository
        self._connection_repository = connection_repository

    def list_users(self) -> List[User]:
        return self._user_repository.list()

    def get_user(self, user_uid: str) -> User:
        user = self._user_repository.get(user_uid)
        if user is None:
            raise ValueError(f"Usuario com uid {user_uid} nao encontrado")
        return user

    def create_user(self, payload: UserCreate) -> User:
        if self._user_repository.get(payload.user_uid):
            raise ValueError(f"UID de usuario '{payload.user_uid}' ja esta em uso")
        if self._user_repository.get_by_username(payload.username):
            raise ValueError(f"Nome de usuario '{payload.username}' ja esta em uso")
        return self._user_repository.create(payload)

    def update_user(self, user_uid: str, payload: UserUpdate) -> User:
        user = self._user_repository.update(user_uid, payload)
        if user is None:
            raise ValueError(f"Usuario com uid {user_uid} nao encontrado")
        return user

    def delete_user(self, user_uid: str) -> None:
        removed = self._user_repository.delete(user_uid)
        if not removed:
            raise ValueError(f"Usuario com uid {user_uid} nao encontrado")

    def connect_users(self, user_uid: str, target_uid: str) -> Connection:
        if user_uid == target_uid:
            raise ValueError("Nao e possivel conectar um usuario a ele mesmo")

        self.get_user(user_uid)
        self.get_user(target_uid)

        if self._connection_repository.exists(user_uid, target_uid):
            raise ValueError("Conexao ja existe entre esses usuarios")

        return self._connection_repository.create(user_uid, target_uid)

    def list_connections(self, user_uid: str) -> List[Connection]:
        self.get_user(user_uid)
        return self._connection_repository.list_by_user(user_uid)


class PostService:
    def __init__(self, post_repository: PostRepository, user_repository: UserRepository):
        self._post_repository = post_repository
        self._user_repository = user_repository

    def list_posts(self) -> List[Post]:
        return self._post_repository.list()

    def get_post(self, post_id: int) -> Post:
        post = self._post_repository.get(post_id)
        if post is None:
            raise ValueError(f"Publicacao com id {post_id} nao encontrada")
        return post

    def create_post(self, payload: PostCreate) -> Post:
        if self._user_repository.get(payload.author_uid) is None:
            raise ValueError(f"Autor com uid {payload.author_uid} nao encontrado")
        if payload.repost_of is not None and self._post_repository.get(payload.repost_of) is None:
            raise ValueError(f"Publicacao original com id {payload.repost_of} nao encontrada")
        return self._post_repository.create(payload)

    def update_post(self, post_id: int, payload: PostUpdate) -> Post:
        post = self._post_repository.update(post_id, payload)
        if post is None:
            raise ValueError(f"Publicacao com id {post_id} nao encontrada")
        return post

    def delete_post(self, post_id: int) -> None:
        removed = self._post_repository.delete(post_id)
        if not removed:
            raise ValueError(f"Publicacao com id {post_id} nao encontrada")

    def list_posts_by_user(self, author_uid: str) -> List[Post]:
        if self._user_repository.get(author_uid) is None:
            raise ValueError(f"Usuario com uid {author_uid} nao encontrado")
        return self._post_repository.list_by_author(author_uid)


class CommentService:
    def __init__(
        self,
        comment_repository: CommentRepository,
        user_repository: UserRepository,
        post_repository: PostRepository,
    ):
        self._comment_repository = comment_repository
        self._user_repository = user_repository
        self._post_repository = post_repository

    def list_comments(self, post_id: int) -> List[Comment]:
        if self._post_repository.get(post_id) is None:
            raise ValueError(f"Publicacao com id {post_id} nao encontrada")
        return self._comment_repository.list_by_post(post_id)

    def create_comment(self, post_id: int, payload: CommentCreate) -> Comment:
        if self._post_repository.get(post_id) is None:
            raise ValueError(f"Publicacao com id {post_id} nao encontrada")
        if self._user_repository.get(payload.author_uid) is None:
            raise ValueError(f"Autor com uid {payload.author_uid} nao encontrado")
        return self._comment_repository.create(post_id, payload)


class RepostService:
    def __init__(
        self,
        repost_repository: RepostRepository,
        user_repository: UserRepository,
        post_repository: PostRepository,
    ):
        self._repost_repository = repost_repository
        self._user_repository = user_repository
        self._post_repository = post_repository

    def list_reposts(self, post_id: int) -> List[Repost]:
        if self._post_repository.get(post_id) is None:
            raise ValueError(f"Publicacao com id {post_id} nao encontrada")
        return self._repost_repository.list_by_post(post_id)

    def create_repost(self, post_id: int, payload: RepostCreate) -> Repost:
        if self._post_repository.get(post_id) is None:
            raise ValueError(f"Publicacao com id {post_id} nao encontrada")
        if self._user_repository.get(payload.user_uid) is None:
            raise ValueError(f"Usuario com uid {payload.user_uid} nao encontrado")
        return self._repost_repository.create(post_id, payload.user_uid)
