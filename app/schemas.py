from datetime import datetime
from typing import Optional
from pydantic import AliasChoices, BaseModel, ConfigDict, Field

# --- User Schemas (Sem alterações) ---
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

    model_config = ConfigDict(from_attributes=True, extra="ignore")


# --- Post Schemas (Alteração principal aqui) ---
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
    # vvvvvv A MUDANÇA MAIS IMPORTANTE ESTÁ AQUI vvvvvv
    author: UserRead  # Trocamos 'author_uid: str' por o objeto completo do autor
    # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    created_at: datetime
    updated_at: datetime
    repost_of: Optional[int] = None

    model_config = ConfigDict(from_attributes=True, extra="ignore")


# --- Comment Schemas (Atualizado para consistência) ---
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
    author: UserRead # <-- Atualizado aqui também
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")


# --- Outros Schemas (Atualizados para consistência) ---
class ConnectionRead(BaseModel):
    id: int
    user: UserRead # <-- Atualizado
    connected_user: UserRead # <-- Atualizado
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
    user: UserRead # <-- Atualizado
    created_at: datetime

    model_config = ConfigDict(from_attributes=True, extra="ignore")