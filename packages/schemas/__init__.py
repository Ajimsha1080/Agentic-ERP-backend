"""
Schemas package.

Pydantic schemas for all API endpoints.
"""

from .tools import (
    ToolCreate,
    ToolUpdate,
    ToolResponse,
    ToolResponseWithConfig,
    ToolExecutionRequest,
    ToolExecutionResponse,
    ToolType,
    ToolStats,
    ToolValidationResponse
)

from .connectors import (
    ConnectorCreate,
    ConnectorUpdate,
    ConnectorResponse,
    ConnectionCreate,
    ConnectionUpdate,
    ConnectionResponse,
    ConnectionStatus,
    ConnectorTestRequest,
    ConnectorTestResponse,
    ConnectorStats,
    ConnectorValidationResponse
)

from .workflows import (
    WorkflowCreate,
    WorkflowUpdate,
    WorkflowResponse,
    WorkflowExecutionRequest,
    WorkflowExecutionResponse,
    WorkflowExecutionCreate,
    WorkflowExecutionUpdate,
    WorkflowExecutionLog,
    WorkflowTemplateCreate,
    WorkflowTemplateResponse,
    WorkflowStats
)

__all__ = [
    # Tool schemas
    "ToolCreate",
    "ToolUpdate",
    "ToolResponse",
    "ToolResponseWithConfig",
    "ToolExecutionRequest",
    "ToolExecutionResponse",
    "ToolType",
    "ToolStats",
    "ToolValidationResponse",
    
    # Connector schemas
    "ConnectorCreate",
    "ConnectorUpdate",
    "ConnectorResponse",
    "ConnectionCreate",
    "ConnectionUpdate",
    "ConnectionResponse",
    "ConnectionStatus",
    "ConnectorTestRequest",
    "ConnectorTestResponse",
    "ConnectorStats",
    "ConnectorValidationResponse",
    
    # Workflow schemas
    "WorkflowCreate",
    "WorkflowUpdate",
    "WorkflowResponse",
    "WorkflowExecutionRequest",
    "WorkflowExecutionResponse",
    "WorkflowExecutionCreate",
    "WorkflowExecutionUpdate",
    "WorkflowExecutionLog",
    "WorkflowTemplateCreate",
    "WorkflowTemplateResponse",
    "WorkflowStats"
]