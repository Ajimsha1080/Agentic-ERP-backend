"""
Tools database models.

Define AI agent tools and their configurations.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.postgresql import UUID as PGUUID

from packages.models.base import BaseModel, TimestampMixin, TenantMixin

Base = declarative_base()


class Tool(BaseModel, TimestampMixin, TenantMixin):
    """AI Agent Tool model."""

    __tablename__ = "tools"

    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, default=None)
    name: str = Column(String(100), nullable=False, unique=True)
    description: Optional[str] = Column(Text, nullable=True)
    type: str = Column(String(50), nullable=False, index=True)  # e.g., "api", "database", "file", "ai", "calculation"
    category: Optional[str] = Column(String(50), nullable=True, index=True)  # e.g., "data", "communication", "productivity"
    version: str = Column(String(20), nullable=False, default="1.0.0")
    config_schema: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # JSON schema for tool configuration
    input_schema: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # JSON schema for inputs
    output_schema: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # JSON schema for outputs
    is_enabled: bool = Column(Boolean, nullable=False, default=True)
    is_public: bool = Column(Boolean, nullable=False, default=False)  # Public tools can be used by all agents
    author: Optional[str] = Column(String(100), nullable=True)  # Tool author/creator
    tags: Optional[List[str]] = Column(JSON, nullable=True)  # Tool tags for search and categorization
    usage_count: int = Column(Integer, nullable=False, default=0)  # Track usage statistics
    last_used_at: Optional[datetime] = Column(DateTime, nullable=True)  # Last usage timestamp

    def __repr__(self):
        return f"<Tool(id={self.id}, name='{self.name}', type='{self.type}', enabled={self.is_enabled})>"


class ToolExecution(BaseModel, TimestampMixin):
    """Tool execution history."""

    __tablename__ = "tool_executions"

    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, default=None)
    tool_id: UUID = Column(PGUUID(as_uuid=True), nullable=False, index=True)
    agent_id: Optional[UUID] = Column(PGUUID(as_uuid=True), nullable=True, index=True)
    user_id: Optional[UUID] = Column(PGUUID(as_uuid=True), nullable=True, index=True)
    input_data: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Input data used for execution
    output_data: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Output data from execution
    status: str = Column(String(50), nullable=False, default="pending")  # pending, running, completed, failed, cancelled
    execution_time: Optional[float] = Column(String, nullable=True)  # Execution time in seconds
    error_message: Optional[str] = Column(Text, nullable=True)  # Error message if execution failed
    metadata: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Additional execution metadata

    def __repr__(self):
        return f"<ToolExecution(id={self.id}, tool_id='{self.tool_id}', status='{self.status}')>"