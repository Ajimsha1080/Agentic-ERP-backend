"""
Connectors database models.

Define external service connectors and integrations.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from packages.models.base import BaseModel, TimestampMixin, TenantMixin

Base = declarative_base()


class Connector(BaseModel, TimestampMixin, TenantMixin):
    """External Service Connector model."""

    __tablename__ = "connectors"

    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, default=None)
    name: str = Column(String(100), nullable=False, unique=True)
    description: Optional[str] = Column(Text, nullable=True)
    service_type: str = Column(String(50), nullable=False, index=True)  # e.g., "email", "storage", "api", "database"
    category: Optional[str] = Column(String(50), nullable=True, index=True)  # e.g., "communication", "storage", "integration"
    version: str = Column(String(20), nullable=False, default="1.0.0")
    config_schema: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # JSON schema for connector configuration
    auth_config: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Authentication configuration
    base_url: Optional[str] = Column(String(255), nullable=True)  # Base URL for external service
    is_enabled: bool = Column(Boolean, nullable=False, default=True)
    is_public: bool = Column(Boolean, nullable=False, default=False)  # Public connectors can be used by all agents
    author: Optional[str] = Column(String(100), nullable=True)  # Connector author/creator
    tags: Optional[List[str]] = Column(JSON, nullable=True)  # Connector tags for search and categorization
    usage_count: int = Column(Integer, nullable=False, default=0)  # Track usage statistics
    last_used_at: Optional[datetime] = Column(DateTime, nullable=True)  # Last usage timestamp

    def __repr__(self):
        return f"<Connector(id={self.id}, name='{self.name}', service_type='{self.service_type}', enabled={self.is_enabled})>"


class Connection(BaseModel, TimestampMixin, TenantMixin):
    """Individual connection instance using a connector."""

    __tablename__ = "connections"

    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, default=None)
    connector_id: UUID = Column(PGUUID(as_uuid=True), nullable=False, index=True)
    user_id: UUID = Column(PGUUID(as_uuid=True), nullable=False, index=True)
    name: str = Column(String(100), nullable=False)  # User-defined connection name
    description: Optional[str] = Column(Text, nullable=True)  # User-defined description
    config: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Connection-specific configuration
    status: str = Column(String(20), nullable=False, default="active")  # active, inactive, error, revoked
    last_connected_at: Optional[datetime] = Column(DateTime, nullable=True)  # Last successful connection timestamp
    metadata: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Additional connection metadata

    # Relationships
    connector = relationship("Connector", foreign_keys=[connector_id])

    def __repr__(self):
        return f"<Connection(id={self.id}, connector_id='{self.connector_id}', name='{self.name}', status='{self.status}')>"


class ConnectionLog(BaseModel, TimestampMixin):
    """Connection activity log."""

    __tablename__ = "connection_logs"

    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, default=None)
    connection_id: UUID = Column(PGUUID(as_uuid=True), nullable=False, index=True)
    action: str = Column(String(50), nullable=False)  # connect, disconnect, query, sync, etc.
    status: str = Column(String(20), nullable=False)  # success, error, warning
    duration: Optional[float] = Column(String, nullable=True)  # Request duration in seconds
    request_data: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Request data
    response_data: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Response data
    error_message: Optional[str] = Column(Text, nullable=True)  # Error message
    metadata: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Additional log metadata

    def __repr__(self):
        return f"<ConnectionLog(id={self.id}, connection_id='{self.connection_id}', action='{self.action}', status='{self.status}')>"