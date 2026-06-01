import re
from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings


def normalize_database_url(url: str) -> str:
    """Easypanel often uses postgres:// — SQLAlchemy needs postgresql+psycopg2://"""
    if url.startswith("sqlite"):
        return url
    if url.startswith("postgres://"):
        return "postgresql+psycopg2://" + url[len("postgres://") :]
    if url.startswith("postgresql://") and not url.startswith("postgresql+"):
        return "postgresql+psycopg2://" + url[len("postgresql://") :]
    return url


def normalized_database_url() -> str:
    return normalize_database_url(settings.DATABASE_URL)


def mask_database_url(url: str) -> str:
    return re.sub(r":([^:@/]+)@", ":***@", url)


_db_url = normalized_database_url()
connect_args = {"check_same_thread": False} if _db_url.startswith("sqlite") else {}

engine = create_engine(
    _db_url,
    connect_args=connect_args,
    pool_pre_ping=True,
    pool_recycle=300,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def init_db() -> None:
    from app.models import order  # noqa: F401

    Base.metadata.create_all(bind=engine)
