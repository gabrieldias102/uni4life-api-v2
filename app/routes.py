from fastapi import APIRouter, HTTPException, status
from typing import List

from app.repositories import (
    CommentRepository,
    ConnectionRepository,
    PostRepository,
    RepostRepository,
    UserRepository,
)
from app.schemas import (
    CommentCreate,
    CommentRead,
    ConnectionRead,
    PostCreate,
    PostRead,
    PostUpdate,
    RepostCreate,
    RepostRead,
    UserCreate,
    UserRead,
    UserUpdate,
)
from app.services import CommentService, PostService, RepostService, UserService

router = APIRouter()

user_repository = UserRepository()
post_repository = PostRepository()
comment_repository = CommentRepository()
repost_repository = RepostRepository()
connection_repository = ConnectionRepository()

user_service = UserService(user_repository, connection_repository)
post_service = PostService(post_repository, user_repository)
comment_service = CommentService(comment_repository, user_repository, post_repository)
repost_service = RepostService(repost_repository, user_repository, post_repository)


def _handle_error(error: ValueError, not_found=False):
    if not_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "ok"}


@router.get("/users", response_model=List[UserRead])
def list_users():
    return user_service.list_users()

@router.get("/users/{user_id}", response_model=UserRead)
def get_user(user_id: int):
    try:
        return user_service.get_user(user_id)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate):
    try:
        return user_service.create_user(payload)
    except ValueError as err:
        _handle_error(err)


@router.put("/users/{user_id}", response_model=UserRead)
def update_user(user_id: int, payload: UserUpdate):
    try:
        return user_service.update_user(user_id, payload)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.delete("/users/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_id: int):
    try:
        user_service.delete_user(user_id)
        return None
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.post(
    "/users/{user_id}/connections/{target_id}",
    response_model=ConnectionRead,
    status_code=status.HTTP_201_CREATED,
)
def connect_users(user_id: int, target_id: int):
    try:
        return user_service.connect_users(user_id, target_id)
    except ValueError as err:
        _handle_error(err)


@router.get("/users/{user_id}/connections", response_model=List[ConnectionRead])
def list_connections(user_id: int):
    try:
        return user_service.list_connections(user_id)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.get("/users/{user_id}/posts", response_model=List[PostRead])
def list_user_posts(user_id: int):
    try:
        return post_service.list_posts_by_user(user_id)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.get("/posts", response_model=List[PostRead])
def list_posts():
    return post_service.list_posts()


@router.get("/posts/{post_id}", response_model=PostRead)
def get_post(post_id: int):
    try:
        return post_service.get_post(post_id)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate):
    try:
        return post_service.create_post(payload)
    except ValueError as err:
        _handle_error(err)


@router.put("/posts/{post_id}", response_model=PostRead)
def update_post(post_id: int, payload: PostUpdate):
    try:
        return post_service.update_post(post_id, payload)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    try:
        post_service.delete_post(post_id)
        return None
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.get("/posts/{post_id}/comments", response_model=List[CommentRead])
def list_post_comments(post_id: int):
    try:
        return comment_service.list_comments(post_id)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.post("/posts/{post_id}/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(post_id: int, payload: CommentCreate):
    try:
        return comment_service.create_comment(post_id, payload)
    except ValueError as err:
        _handle_error(err)


@router.get("/posts/{post_id}/reposts", response_model=List[RepostRead])
def list_post_reposts(post_id: int):
    try:
        return repost_service.list_reposts(post_id)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.post("/posts/{post_id}/reposts", response_model=RepostRead, status_code=status.HTTP_201_CREATED)
def create_repost(post_id: int, payload: RepostCreate):
    try:
        return repost_service.create_repost(post_id, payload)
    except ValueError as err:
        _handle_error(err)
