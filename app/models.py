from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class User:
    id: int
    full_name: str
    username: str
    bio: Optional[str]
    joined_at: datetime
    updated_at: datetime


@dataclass
class Post:
    id: int
    author_id: int
    content: str
    created_at: datetime
    updated_at: datetime
    repost_of: Optional[int] = None


@dataclass
class Comment:
    id: int
    post_id: int
    author_id: int
    content: str
    created_at: datetime


@dataclass
class Repost:
    id: int
    post_id: int
    user_id: int
    created_at: datetime


@dataclass
class Connection:
    id: int
    user_id: int
    connected_user_id: int
    created_at: datetime
