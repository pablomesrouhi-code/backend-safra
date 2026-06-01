import logging
import re
import threading
from collections.abc import Generator

from sqlalchemy import create_engine, text
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.core.config import settings

logger = logging.getLogger(__name__)

_db_lock = threading.Lock()
_db_ready = False


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


def is_db_ready() -> bool:
    return _db_ready


def init_db() -> None:
    global _db_ready
    from app.models import order  # noqa: F401

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    Base.metadata.create_all(bind=engine)
    _db_ready = True
    logger.info("Database tables ready")


def try_init_db() -> bool:
    """Idempotent — safe to call from background retry loop."""
    global _db_ready
    if _db_ready:
        return True
    with _db_lock:
        if _db_ready:
            return True
        try:
            init_db()
            return True
        except SQLAlchemyError as exc:
            logger.warning("Database connection failed: %s", exc)
            return False
        except Exception as exc:
            logger.exception("Database init error: %s", exc)
            return False


def get_db() -> Generator[Session, None, None]:
    if not _db_ready:
        try_init_db()
    if not _db_ready:
        raise RuntimeError(
            "Database not ready. Set DATABASE_URL in Easypanel (postgres://...@safraskin_database:5432/...)"
        )
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
