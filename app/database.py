from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from app.config import get_settings


class Base(DeclarativeBase):
    pass


def _normalize_database_url(database_url: str) -> str:
    if database_url.startswith("postgresql+psycopg://"):
        return database_url
    if database_url.startswith("postgresql://"):
        return database_url.replace("postgresql://", "postgresql+psycopg://", 1)
    if database_url.startswith("postgres://"):
        return database_url.replace("postgres://", "postgresql+psycopg://", 1)
    return database_url


settings = get_settings()
database_url = _normalize_database_url(settings.database_url)

connect_args: dict[str, object] = {}
engine_kwargs: dict[str, object] = {
    "echo": settings.db_echo,
    "pool_pre_ping": True,
}

if database_url.startswith("sqlite"):
    connect_args["check_same_thread"] = False

if connect_args:
    engine_kwargs["connect_args"] = connect_args

engine = create_engine(database_url, **engine_kwargs)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
    expire_on_commit=False,
)


def init_db() -> None:
    # Import models lazily so all ORM tables are registered before create_all runs.
    from app import models  # noqa: F401

    Base.metadata.create_all(bind=engine)
