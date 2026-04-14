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

    def get_user(self, user_id: int) -> User:
        user = self._user_repository.get(user_id)
        if user is None:
            raise ValueError(f"Usuário com id {user_id} não encontrado")
        return user

    def create_user(self, payload: UserCreate) -> User:
        if self._user_repository.get_by_username(payload.username):
            raise ValueError(f"Nome de usuário '{payload.username}' já está em uso")
        return self._user_repository.create(payload)

    def update_user(self, user_id: int, payload: UserUpdate) -> User:
        user = self._user_repository.update(user_id, payload)
        if user is None:
            raise ValueError(f"Usuário com id {user_id} não encontrado")
        return user

    def delete_user(self, user_id: int) -> None:
        removed = self._user_repository.delete(user_id)
        if not removed:
            raise ValueError(f"Usuário com id {user_id} não encontrado")

    def connect_users(self, user_id: int, target_id: int) -> Connection:
        if user_id == target_id:
            raise ValueError("Não é possível conectar um usuário a ele mesmo")

        self.get_user(user_id)
        self.get_user(target_id)

        if self._connection_repository.exists(user_id, target_id):
            raise ValueError("Conexão já existe entre esses usuários")

        return self._connection_repository.create(user_id, target_id)

    def list_connections(self, user_id: int) -> List[Connection]:
        self.get_user(user_id)
        return self._connection_repository.list_by_user(user_id)


class PostService:
    def __init__(self, post_repository: PostRepository, user_repository: UserRepository):
        self._post_repository = post_repository
        self._user_repository = user_repository

    def list_posts(self) -> List[Post]:
        return self._post_repository.list()

    def get_post(self, post_id: int) -> Post:
        post = self._post_repository.get(post_id)
        if post is None:
            raise ValueError(f"Publicação com id {post_id} não encontrada")
        return post

    def create_post(self, payload: PostCreate) -> Post:
        if self._user_repository.get(payload.author_id) is None:
            raise ValueError(f"Autor com id {payload.author_id} não encontrado")
        if payload.repost_of is not None and self._post_repository.get(payload.repost_of) is None:
            raise ValueError(f"Publicação original com id {payload.repost_of} não encontrada")
        return self._post_repository.create(payload)

    def update_post(self, post_id: int, payload: PostUpdate) -> Post:
        post = self._post_repository.update(post_id, payload)
        if post is None:
            raise ValueError(f"Publicação com id {post_id} não encontrada")
        return post

    def delete_post(self, post_id: int) -> None:
        removed = self._post_repository.delete(post_id)
        if not removed:
            raise ValueError(f"Publicação com id {post_id} não encontrada")

    def list_posts_by_user(self, author_id: int) -> List[Post]:
        if self._user_repository.get(author_id) is None:
            raise ValueError(f"Usuário com id {author_id} não encontrado")
        return self._post_repository.list_by_author(author_id)


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
            raise ValueError(f"Publicação com id {post_id} não encontrada")
        return self._comment_repository.list_by_post(post_id)

    def create_comment(self, post_id: int, payload: CommentCreate) -> Comment:
        if self._post_repository.get(post_id) is None:
            raise ValueError(f"Publicação com id {post_id} não encontrada")
        if self._user_repository.get(payload.author_id) is None:
            raise ValueError(f"Autor com id {payload.author_id} não encontrado")
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
            raise ValueError(f"Publicação com id {post_id} não encontrada")
        return self._repost_repository.list_by_post(post_id)

    def create_repost(self, post_id: int, payload: RepostCreate) -> Repost:
        if self._post_repository.get(post_id) is None:
            raise ValueError(f"Publicação com id {post_id} não encontrada")
        if self._user_repository.get(payload.user_id) is None:
            raise ValueError(f"Usuário com id {payload.user_id} não encontrado")
        return self._repost_repository.create(post_id, payload.user_id)
