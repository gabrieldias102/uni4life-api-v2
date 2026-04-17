from datetime import datetime

from sqlalchemy import CheckConstraint, DateTime, ForeignKey, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.database import Base


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_uid: Mapped[str] = mapped_column(String(128), nullable=False, unique=True, index=True)
    full_name: Mapped[str] = mapped_column(String(120), nullable=False)
    username: Mapped[str] = mapped_column(String(40), nullable=False, unique=True, index=True)
    bio: Mapped[str | None] = mapped_column(String(240), nullable=True)
    joined_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )


class Post(Base):
    __tablename__ = "posts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    author_uid: Mapped[str] = mapped_column(ForeignKey("users.user_uid", ondelete="CASCADE"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(Text, nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=False),
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False,
    )
    repost_of: Mapped[int | None] = mapped_column(ForeignKey("posts.id", ondelete="SET NULL"), nullable=True)


class Comment(Base):
    __tablename__ = "comments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    author_uid: Mapped[str] = mapped_column(ForeignKey("users.user_uid", ondelete="CASCADE"), nullable=False, index=True)
    content: Mapped[str] = mapped_column(String(500), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)


class Repost(Base):
    __tablename__ = "reposts"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    post_id: Mapped[int] = mapped_column(ForeignKey("posts.id", ondelete="CASCADE"), nullable=False, index=True)
    user_uid: Mapped[str] = mapped_column(ForeignKey("users.user_uid", ondelete="CASCADE"), nullable=False, index=True)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)


class Connection(Base):
    __tablename__ = "connections"
    __table_args__ = (
        CheckConstraint("user_uid < connected_user_uid", name="ck_connections_order"),
        UniqueConstraint("user_uid", "connected_user_uid", name="uq_connections_pair"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_uid: Mapped[str] = mapped_column(ForeignKey("users.user_uid", ondelete="CASCADE"), nullable=False)
    connected_user_uid: Mapped[str] = mapped_column(ForeignKey("users.user_uid", ondelete="CASCADE"), nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=False), default=datetime.utcnow, nullable=False)
