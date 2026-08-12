"""
Workflows database models.

Define AI agent workflows and their executions.
"""

from datetime import datetime
from typing import Optional, List, Dict, Any
from uuid import UUID
from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID as PGUUID
from sqlalchemy import Enum as SQLEnum
import enum

from packages.models.base import BaseModel, TimestampMixin, TenantMixin

Base = declarative_base()


class WorkflowStatus(enum.Enum):
    """Workflow status enum."""
    DRAFT = "draft"
    ACTIVE = "active"
    PAUSED = "paused"
    ARCHIVED = "archived"


class WorkflowExecutionStatus(enum.Enum):
    """Workflow execution status enum."""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    STOPPED = "stopped"
    CANCELLED = "cancelled"


class Workflow(BaseModel, TimestampMixin, TenantMixin):
    """AI Agent Workflow model."""

    __tablename__ = "workflows"

    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, default=None)
    name: str = Column(String(100), nullable=False, unique=True)
    description: Optional[str] = Column(Text, nullable=True)
    agent_id: UUID = Column(PGUUID(as_uuid=True), nullable=False, index=True)
    category: Optional[str] = Column(String(50), nullable=True, index=True)  # e.g., "data_processing", "reporting", "automation"
    version: str = Column(String(20), nullable=False, default="1.0.0")
    status: WorkflowStatus = Column(SQLEnum(WorkflowStatus), nullable=False, default=WorkflowStatus.ACTIVE)
    config_schema: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # JSON schema for workflow configuration
    input_schema: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # JSON schema for inputs
    output_schema: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # JSON schema for outputs
    steps: Optional[List[Dict[str, Any]]] = Column(JSON, nullable=True)  # Workflow steps definition
    triggers: Optional[List[Dict[str, Any]]] = Column(JSON, nullable=True)  # Workflow triggers
    schedule: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Schedule configuration
    is_enabled: bool = Column(Boolean, nullable=False, default=True)
    is_public: bool = Column(Boolean, nullable=False, default=False)  # Public workflows can be used by all agents
    author: Optional[str] = Column(String(100), nullable=True)  # Workflow author/creator
    tags: Optional[List[str]] = Column(JSON, nullable=True)  # Workflow tags for search and categorization
    usage_count: int = Column(Integer, nullable=False, default=0)  # Track usage statistics
    last_used_at: Optional[datetime] = Column(DateTime, nullable=True)  # Last usage timestamp

    def __repr__(self):
        return f"<Workflow(id={self.id}, name='{self.name}', status='{self.status.value}', enabled={self.is_enabled})>"


class WorkflowExecution(BaseModel, TimestampMixin):
    """Workflow execution history."""

    __tablename__ = "workflow_executions"

    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, default=None)
    workflow_id: UUID = Column(PGUUID(as_uuid=True), nullable=False, index=True)
    user_id: UUID = Column(PGUUID(as_uuid=True), nullable=False, index=True)
    agent_id: UUID = Column(PGUUID(as_uuid=True), nullable=True, index=True)
    trigger_type: Optional[str] = Column(String(50), nullable=True)  # manual, scheduled, webhook, etc.
    input_data: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Input data used for execution
    output_data: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Output data from execution
    status: WorkflowExecutionStatus = Column(SQLEnum(WorkflowExecutionStatus), nullable=False, default=WorkflowExecutionStatus.PENDING)
    started_at: Optional[datetime] = Column(DateTime, nullable=True)  # Execution start timestamp
    completed_at: Optional[datetime] = Column(DateTime, nullable=True)  # Execution completion timestamp
    execution_time: Optional[float] = Column(String, nullable=True)  # Total execution time in seconds
    current_step: Optional[int] = Column(Integer, nullable=True)  # Current step index
    total_steps: Optional[int] = Column(Integer, nullable=True)  # Total number of steps
    error_message: Optional[str] = Column(Text, nullable=True)  # Error message if execution failed
    logs: Optional[List[Dict[str, Any]]] = Column(JSON, nullable=True)  # Execution logs
    metadata: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # Additional execution metadata

    def __repr__(self):
        return f"<WorkflowExecution(id={self.id}, workflow_id='{self.workflow_id}', status='{self.status.value}')>"


class WorkflowTemplate(BaseModel, TimestampMixin, TenantMixin):
    """Workflow templates that can be used to create new workflows."""

    __tablename__ = "workflow_templates"

    id: UUID = Column(PGUUID(as_uuid=True), primary_key=True, default=None)
    name: str = Column(String(100), nullable=False, unique=True)
    description: Optional[str] = Column(Text, nullable=True)
    category: Optional[str] = Column(String(50), nullable=True, index=True)  # e.g., "data_processing", "reporting", "automation"
    version: str = Column(String(20), nullable=False, default="1.0.0")
    config_schema: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # JSON schema for workflow configuration
    input_schema: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # JSON schema for inputs
    output_schema: Optional[Dict[str, Any]] = Column(JSON, nullable=True)  # JSON schema for outputs
    steps: Optional[List[Dict[str, Any]]] = Column(JSON, nullable=True)  # Workflow steps definition
    triggers: Optional[List[Dict[str, Any]]] = Column(JSON, nullable=True)  # Workflow triggers
    tags: Optional[List[str]] = Column(JSON, nullable=True)  # Template tags for search and categorization
    usage_count: int = Column(Integer, nullable=False, default=0)  # Track usage statistics
    author: Optional[str] = Column(String(100), nullable=True)  # Template author/creator

    def __repr__(self):
        return f"<WorkflowTemplate(id={self.id}, name='{self.name}', category='{self.category}')>"