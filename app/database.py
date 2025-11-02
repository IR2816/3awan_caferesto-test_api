import logging
import os
from dotenv import load_dotenv
from sqlmodel import SQLModel, create_engine, Session

# Load .env (if present) so DATABASE_URL can be read during local development
load_dotenv()

DATABASE_URL = os.getenv("DATABASE_URL")
if not DATABASE_URL:
    # Be permissive for local dev — caller can set a test engine via set_engine().
    DATABASE_URL = None

logger = logging.getLogger(__name__)
logger.info("Initializing database module")

# create default engine if DATABASE_URL is provided
def _create_engine(url: str):
    # SQLite requires check_same_thread for in-memory usage; Postgres does not
    if url.startswith("sqlite"):
        return create_engine(url, echo=False, connect_args={"check_same_thread": False})
    return create_engine(url, echo=False, pool_pre_ping=True)

engine = None
if DATABASE_URL:
    engine = _create_engine(DATABASE_URL)

def set_engine(new_engine):
    """Replace the module-level engine (used by other modules). Useful for tests/dev.

    Example:
        from app import database
        database.set_engine(engine)
    """
    global engine
    engine = new_engine

def get_engine():
    return engine


def init_db():
    """Create database tables from SQLModel metadata using the active engine.

    This is a convenience for quick local setups. For production environments
    prefer proper migrations (Alembic) and do not call this at runtime.
    """
    if engine is None:
        raise RuntimeError("Database engine is not configured. Set DATABASE_URL or call set_engine().")
    SQLModel.metadata.create_all(engine)


def get_session():
    if engine is None:
        raise RuntimeError("Database engine is not configured. Set DATABASE_URL or call set_engine().")
    with Session(engine) as session:
        yield session
