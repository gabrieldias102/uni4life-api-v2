from datetime import datetime
from typing import Optional
from pydantic import AliasChoices, BaseModel, ConfigDict, Field


class UserBase(BaseModel):
    full_name: str = Field(min_length=3, max_length=120)
    username: str = Field(min_length=3, max_length=40)
    bio: Optional[str] = Field(None, max_length=240)

class UserCreate(UserBase):
    user_uid: str = Field(min_length=1, max_length=128, validation_alias=AliasChoices("user_uid", "uid", "user_id"))

class UserUpdate(BaseModel):
    full_name: Optional[str] = Field(None, min_length=3, max_length=120)
    bio: Optional[str] = Field(None, max_length=240)

class UserRead(UserBase):
    user_uid: str
    joined_at: datetime
    updated_at: datetime
    
    post_count: int = 0
    connection_count: int = 0

    model_config = ConfigDict(from_attributes=True, extra="ignore")


class PostBase(BaseModel):
    content: str = Field(..., min_length=1, max_length=1000)

class PostCreate(PostBase):
    author_uid: str = Field(
        min_length=1,
        max_length=128,
        validation_alias=AliasChoices("author_uid", "user_uid", "author_id", "user_id"),
    )
    repost_of: Optional[int] = None

class PostUpdate(BaseModel):
    content: Optional[str] = Field(None, min_length=1, max_length=1000)

class PostRead(PostBase):
    id: int
    
    author: UserRead  
    
    created_at: datetime
    updated_at: datetime
    repost_of: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")



class CommentCreate(BaseModel):
    author_uid: str = Field(
        min_length=1,
        max_length=128,
        validation_alias=AliasChoices("author_uid", "user_uid", "author_id", "user_id"),
    )
    content: str = Field(..., min_length=1, max_length=500)

class CommentRead(BaseModel):
    id: int
    post_id: int
    author: UserRead 
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")



class ConnectionRead(BaseModel):
    id: int
    user: UserRead 
    connected_user: UserRead 
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")

class RepostCreate(BaseModel):
    user_uid: str = Field(
        min_length=1,
        max_length=128,
        validation_alias=AliasChoices("user_uid", "user_id"),
    )

class RepostRead(BaseModel):
    id: int
    post_id: int
    user: UserRead 
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")