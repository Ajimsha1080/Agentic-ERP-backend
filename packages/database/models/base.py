from datetime import datetime
from typing import Any, Dict, Optional
from uuid import UUID, uuid4

from sqlalchemy import Column, DateTime, String, Text, Boolean, JSON, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID as PG_UUID
from sqlalchemy.orm import declared_attr



class TimestampMixin:
    """Mixin to add created_at and updated_at timestamps."""

    @declared_attr
    def created_at(cls) -> Column:
        return Column(DateTime, default=datetime.utcnow, nullable=False)

    @declared_attr
    def updated_at(cls) -> Column:
        return Column(
            DateTime,
            default=datetime.utcnow,
            onupdate=datetime.utcnow,
            nullable=False
        )


class UUIDMixin:
    """Mixin to add UUID primary key."""

    @declared_attr
    def id(cls) -> Column:
        return Column(
            PG_UUID(as_uuid=True),
            primary_key=True,
            default=uuid4,
            nullable=False
        )


class TenantScopedMixin:
    """Mixin to add tenant-scoped properties."""

    @declared_attr
    def tenant_id(cls) -> Column:
        return Column(
            PG_UUID(as_uuid=True),
            ForeignKey('organizations.id', ondelete='CASCADE'),
            nullable=False,
            index=True
        )


class SoftDeleteMixin:
    """Mixin for soft delete functionality."""

    @declared_attr
    def is_deleted(cls) -> Column:
        return Column(Boolean, default=False, nullable=False)

    @declared_attr
    def deleted_at(cls) -> Column:
        return Column(DateTime, nullable=True)


class TenantIDMixin(TenantScopedMixin, UUIDMixin, TimestampMixin):
    """Mixin combining tenant scoping with UUID and timestamps."""

    pass


class Base(UUIDMixin, TimestampMixin):
    """Base model class for all database models."""

    __abstract__ = True

    @declared_attr
    def __tablename__(cls) -> str:
        """Generate table name from class name."""
        return cls.__name__.lower() + 's'

    def to_dict(self, exclude: Optional[list] = None) -> Dict[str, Any]:
        """Convert model instance to dictionary."""
        if exclude is None:
            exclude = []

        data = {}
        for column in self.__table__.columns:
            if column.name not in exclude:
                value = getattr(self, column.name)
                # Convert UUID to string
                if isinstance(value, UUID):
                    value = str(value)
                data[column.name] = value
        return data


# Create indexes for common query patterns
class IndexMixin:
    """Mixin to create database indexes."""

    @classmethod
    def __table_args__(cls):
        """Define table-specific indexes."""
        indexes = []
        for attr_name, index_config in cls.__dict__.items():
            if attr_name.startswith('ix_'):
                indexes.append(index_config)
        return tuple(indexes) or None
