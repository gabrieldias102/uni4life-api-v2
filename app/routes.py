from typing import List

from fastapi import APIRouter, Depends, HTTPException, status

from app.deps import get_comment_service, get_post_service, get_repost_service, get_user_service
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


def _handle_error(error: ValueError, not_found=False):
    if not_found:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error))
    raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(error))


@router.get("/health", status_code=status.HTTP_200_OK)
def health():
    return {"status": "ok"}


@router.get("/users", response_model=List[UserRead])
def list_users(user_service: UserService = Depends(get_user_service)):
    return user_service.list_users()


@router.get("/users/{user_uid}", response_model=UserRead)
def get_user(user_uid: str, user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.get_user(user_uid)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
def create_user(payload: UserCreate, user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.create_user(payload)
    except ValueError as err:
        _handle_error(err)


@router.put("/users/{user_uid}", response_model=UserRead)
def update_user(
    user_uid: str,
    payload: UserUpdate,
    user_service: UserService = Depends(get_user_service),
):
    try:
        return user_service.update_user(user_uid, payload)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.delete("/users/{user_uid}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(user_uid: str, user_service: UserService = Depends(get_user_service)):
    try:
        user_service.delete_user(user_uid)
        return None
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.post(
    "/users/{user_uid}/connections/{target_uid}",
    response_model=ConnectionRead,
    status_code=status.HTTP_201_CREATED,
)
def connect_users(
    user_uid: str,
    target_uid: str,
    user_service: UserService = Depends(get_user_service),
):
    try:
        return user_service.connect_users(user_uid, target_uid)
    except ValueError as err:
        _handle_error(err)


@router.get("/users/{user_uid}/connections", response_model=List[ConnectionRead])
def list_connections(user_uid: str, user_service: UserService = Depends(get_user_service)):
    try:
        return user_service.list_connections(user_uid)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.get("/users/{user_uid}/posts", response_model=List[PostRead])
def list_user_posts(user_uid: str, post_service: PostService = Depends(get_post_service)):
    try:
        return post_service.list_posts_by_user(user_uid)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.get("/posts", response_model=List[PostRead])
def list_posts(post_service: PostService = Depends(get_post_service)):
    return post_service.list_posts()


@router.get("/posts/{post_id}", response_model=PostRead)
def get_post(post_id: int, post_service: PostService = Depends(get_post_service)):
    try:
        return post_service.get_post(post_id)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.post("/posts", response_model=PostRead, status_code=status.HTTP_201_CREATED)
def create_post(payload: PostCreate, post_service: PostService = Depends(get_post_service)):
    try:
        return post_service.create_post(payload)
    except ValueError as err:
        _handle_error(err)


@router.put("/posts/{post_id}", response_model=PostRead)
def update_post(
    post_id: int,
    payload: PostUpdate,
    post_service: PostService = Depends(get_post_service),
):
    try:
        return post_service.update_post(post_id, payload)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.delete("/posts/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, post_service: PostService = Depends(get_post_service)):
    try:
        post_service.delete_post(post_id)
        return None
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.get("/posts/{post_id}/comments", response_model=List[CommentRead])
def list_post_comments(post_id: int, comment_service: CommentService = Depends(get_comment_service)):
    try:
        return comment_service.list_comments(post_id)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.post("/posts/{post_id}/comments", response_model=CommentRead, status_code=status.HTTP_201_CREATED)
def create_comment(
    post_id: int,
    payload: CommentCreate,
    comment_service: CommentService = Depends(get_comment_service),
):
    try:
        return comment_service.create_comment(post_id, payload)
    except ValueError as err:
        _handle_error(err)


@router.get("/posts/{post_id}/reposts", response_model=List[RepostRead])
def list_post_reposts(post_id: int, repost_service: RepostService = Depends(get_repost_service)):
    try:
        return repost_service.list_reposts(post_id)
    except ValueError as err:
        _handle_error(err, not_found=True)


@router.post("/posts/{post_id}/reposts", response_model=RepostRead, status_code=status.HTTP_201_CREATED)
def create_repost(
    post_id: int,
    payload: RepostCreate,
    repost_service: RepostService = Depends(get_repost_service),
):
    try:
        return repost_service.create_repost(post_id, payload)
    except ValueError as err:
        _handle_error(err)
