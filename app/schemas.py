from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field, constr


class UserBase(BaseModel):
    full_name: constr(min_length=3, max_length=120)
    username: constr(min_length=3, max_length=40)
    bio: Optional[str] = Field(None, max_length=240)


class UserCreate(UserBase):
    pass


class UserUpdate(BaseModel):
    full_name: Optional[constr(min_length=3, max_length=120)] = None
    bio: Optional[str] = Field(None, max_length=240)


class UserRead(UserBase):
    id: int
    joined_at: datetime
    updated_at: datetime

    model_config = {"extra": "ignore"}


class ConnectionRead(BaseModel):
    id: int
    user_id: int
    connected_user_id: int
    created_at: datetime

    model_config = {"extra": "ignore"}


class PostBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)


class PostCreate(PostBase):
    author_id: int
    repost_of: Optional[int] = None


class PostUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=1000)


class PostRead(PostBase):
    id: int
    author_id: int
    created_at: datetime
    updated_at: datetime
    repost_of: Optional[int] = None

    model_config = {"extra": "ignore"}


class CommentCreate(BaseModel):
    author_id: int
    content: str = Field(..., min_length=1, max_length=500)


class CommentRead(BaseModel):
    id: int
    post_id: int
    author_id: int
    content: str
    created_at: datetime

    model_config = {"extra": "ignore"}


class RepostCreate(BaseModel):
    user_id: int


class RepostRead(BaseModel):
    id: int
    post_id: int
    user_id: int
    created_at: datetime

    model_config = {"extra": "ignore"}
