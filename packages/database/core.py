"""
Database core functionality.

Provides database connections, session management, and initialization.
"""

from contextlib import contextmanager
from typing import Generator, Optional
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session, declarative_base
import os
import sys

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from .models import Base

# Database URL
DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql://agentic_user:agentic_password@localhost:5432/agentic_platform"
)

# Async Database URL
ASYNC_DATABASE_URL = DATABASE_URL.replace("postgresql://", "postgresql+asyncpg://")


# Create async engine
async_engine = create_async_engine(
    ASYNC_DATABASE_URL,
    echo=os.getenv("ENVIRONMENT", "development") == "development",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create async session factory
AsyncSessionLocal = async_sessionmaker(
    async_engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)


# Create sync engine for worker/background tasks
engine = create_engine(
    DATABASE_URL,
    echo=os.getenv("ENVIRONMENT", "development") == "development",
    pool_size=10,
    max_overflow=20,
    pool_pre_ping=True,
    pool_recycle=3600,
)

# Create session factory for sync
SessionLocal = sessionmaker(
    engine,
    class_=Session,
    expire_on_commit=False,
)


Base = declarative_base()


def get_db() -> Generator[AsyncSession, None, None]:
    """
    Get database session for async operations.

    Yields:
        AsyncSession: Database session

    Example:
        ```python
        db = get_db()
        try:
            # Use db
            user = db.query(User).first()
        finally:
            db.close()
        ```
    """
    session = AsyncSessionLocal()
    try:
        yield session
    finally:
        session.close()


def get_sync_db() -> Generator[Session, None, None]:
    """
    Get database session for sync operations.

    Yields:
        Session: Database session

    Example:
        ```python
        db = get_sync_db()
        try:
            # Use db
            user = db.query(User).first()
        finally:
            db.close()
        ```
    """
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


async def get_engine() -> AsyncSessionLocal:
    """
    Get the async database engine.

    Returns:
        AsyncSessionLocal: Async session factory
    """
    return AsyncSessionLocal


async def create_db_and_tables() -> None:
    """
    Create database and all tables.

    This should only be called during initialization.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def drop_all_tables() -> None:
    """
    Drop all tables.

    This should only be called during testing or cleanup.
    """
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)


def init_database() -> None:
    """
    Initialize database with all tables.
    """
    Base.metadata.create_all(bind=engine)


def reset_database() -> None:
    """
    Reset database - drop all tables and recreate.
    """
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


@contextmanager
def session_scope() -> Generator[Session, None, None]:
    """
    Provide a transactional scope around a series of operations.

    Yields:
        Session: Database session

    Example:
        ```python
        with session_scope() as db:
            user = User(name="John")
            db.add(user)
            # Session is automatically committed
        ```
    """
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


async def async_session_scope() -> Generator[AsyncSession, None, None]:
    """
    Provide a transactional scope for async operations.

    Yields:
        AsyncSession: Async database session

    Example:
        ```python
        async with async_session_scope() as db:
            user = User(name="John")
            db.add(user)
            # Session is automatically committed
        ```
    """
    session = AsyncSessionLocal()
    try:
        yield session
        await session.commit()
    except Exception:
        await session.rollback()
        raise
    finally:
        await session.close()
