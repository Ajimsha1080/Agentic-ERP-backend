"""Agent-related schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field, ConfigDict, HttpUrl
from datetime import datetime
from uuid import UUID

from .base import UUIDResponse, PaginationParams, PaginatedResponse


class AgentCreate(BaseModel):
    """Agent creation schema.

    Args:
        name: Agent name
        slug: Agent slug
        description: Agent description
        display_name: Display name
        icon: Icon (emoji or name)
        type: Agent type
        workspace_id: Workspace ID (optional)
        business_unit_id: Business unit ID (optional)
        model_provider: LLM provider
        model_name: Model name
        model_temperature: Model temperature
        model_max_tokens: Maximum tokens
        system_prompt: System prompt
        requires_approval: Whether approval is required
        approval_threshold: Approval threshold amount
    """

    name: str = Field(..., min_length=1, max_length=255, description="Agent name")
    slug: str = Field(..., min_length=1, max_length=100, description="Agent slug")
    description: Optional[str] = Field(None, description="Agent description")
    display_name: Optional[str] = Field(None, max_length=255, description="Display name")
    icon: Optional[str] = Field(None, max_length=100, description="Icon (emoji or name)")
    type: str = Field(..., description="Agent type")
    workspace_id: Optional[UUID] = Field(None, description="Workspace ID")
    business_unit_id: Optional[UUID] = Field(None, description="Business unit ID")
    model_provider: Optional[str] = Field(None, description="LLM provider")
    model_name: Optional[str] = Field(None, max_length=100, description="Model name")
    model_temperature: float = Field(0.7, ge=0, le=2, description="Model temperature")
    model_max_tokens: int = Field(4000, ge=1, description="Maximum tokens")
    system_prompt: Optional[str] = Field(None, description="System prompt")
    requires_approval: bool = Field(False, description="Whether approval is required")
    approval_threshold: Optional[int] = Field(None, description="Approval threshold amount")


class AgentUpdate(BaseModel):
    """Agent update schema.

    Args:
        name: Agent name
        description: Agent description
        display_name: Display name
        icon: Icon
        model_temperature: Model temperature
        model_max_tokens: Maximum tokens
        system_prompt: System prompt
        requires_approval: Whether approval is required
        approval_threshold: Approval threshold amount
    """

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None
    display_name: Optional[str] = Field(None, max_length=255)
    icon: Optional[str] = Field(None, max_length=100)
    model_temperature: Optional[float] = Field(None, ge=0, le=2)
    model_max_tokens: Optional[int] = Field(None, ge=1)
    system_prompt: Optional[str] = None
    requires_approval: Optional[bool] = None
    approval_threshold: Optional[int] = None


class AgentResponse(BaseModel):
    """Agent response schema.

    Args:
        id: Agent ID
        name: Agent name
        slug: Agent slug
        description: Agent description
        display_name: Display name
        icon: Icon
        type: Agent type
        status: Agent status
        is_active: Whether agent is active
        model_provider: LLM provider
        model_name: Model name
        model_temperature: Model temperature
        model_max_tokens: Maximum tokens
        requires_approval: Whether approval is required
        approval_threshold: Approval threshold amount
        success_rate: Success rate (0-1)
        total_executions: Total executions
        successful_executions: Successful executions
        failed_executions: Failed executions
        average_latency_seconds: Average latency in seconds
        total_tokens_used: Total tokens used
        total_cost: Total cost
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    display_name: Optional[str] = None
    icon: Optional[str] = None
    type: str
    status: str
    is_active: bool
    model_provider: Optional[str] = None
    model_name: Optional[str] = None
    model_temperature: float
    model_max_tokens: int
    requires_approval: bool
    approval_threshold: Optional[int] = None
    success_rate: Optional[float] = None
    total_executions: int
    successful_executions: int
    failed_executions: int
    average_latency_seconds: Optional[float] = None
    total_tokens_used: int
    total_cost: float
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class AgentCreateResponse(UUIDResponse):
    """Agent creation response.

    Inherits from UUIDResponse.
    """

    agent: AgentResponse


class AgentExecutionCreate(BaseModel):
    """Agent execution creation schema.

    Args:
        agent_id: Agent ID
        prompt: Execution prompt
        parameters: Optional parameters
        context: Optional context
    """

    agent_id: UUID = Field(..., description="Agent ID")
    prompt: str = Field(..., min_length=1, description="Execution prompt")
    parameters: Optional[dict] = Field(None, description="Execution parameters")
    context: Optional[dict] = Field(None, description="Execution context")


class AgentExecutionResponse(BaseModel):
    """Agent execution response schema.

    Args:
        id: Execution ID
        agent_id: Agent ID
        user_id: User ID
        status: Execution status
        prompt: Execution prompt
        prompt_tokens: Prompt tokens used
        prompt_model: Model used for prompt
        output: Execution output
        output_tokens: Output tokens used
        error_message: Error message (if any)
        execution_steps: Execution steps
        tools_used: Tools used
        knowledge_used: Knowledge bases used
        started_at: Started timestamp
        completed_at: Completed timestamp
        duration_seconds: Duration in seconds
        retry_count: Retry count
    """

    id: UUID
    agent_id: UUID
    user_id: Optional[UUID] = None
    status: str
    prompt: Optional[str] = None
    prompt_tokens: Optional[int] = None
    prompt_model: Optional[str] = None
    output: Optional[str] = None
    output_tokens: Optional[int] = None
    error_message: Optional[str] = None
    execution_steps: Optional[list] = None
    tools_used: Optional[list] = None
    knowledge_used: Optional[list] = None
    started_at: datetime
    completed_at: Optional[datetime] = None
    duration_seconds: Optional[int] = None
    retry_count: int

    model_config = ConfigDict(from_attributes=True)


class AgentToolResponse(BaseModel):
    """Agent tool response schema.

    Args:
        id: Tool ID
        agent_id: Agent ID
        tool_id: Tool ID
        enabled: Whether tool is enabled
        tool_config: Tool configuration
    """

    id: UUID
    agent_id: UUID
    tool_id: UUID
    enabled: bool
    tool_config: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)


class ToolCreate(BaseModel):
    """Tool creation schema.

    Args:
        name: Tool name
        slug: Tool slug
        description: Tool description
        category: Tool category
        implementation_type: Implementation type
        endpoint_url: API endpoint URL (if applicable)
        endpoint_method: API endpoint method
        input_schema: Input schema (JSON Schema)
        output_schema: Output schema (JSON Schema)
        auth_required: Whether authentication is required
        permission_level: Permission level
        risk_level: Risk level
        requires_approval: Whether approval is required
    """

    name: str = Field(..., min_length=1, max_length=255, description="Tool name")
    slug: str = Field(..., min_length=1, max_length=100, description="Tool slug")
    description: Optional[str] = Field(None, description="Tool description")
    category: str = Field(..., description="Tool category")
    implementation_type: str = Field(..., description="Implementation type")
    endpoint_url: Optional[str] = Field(None, max_length=500, description="API endpoint URL")
    endpoint_method: Optional[str] = Field(None, description="API endpoint method")
    input_schema: Optional[dict] = Field(None, description="Input schema")
    output_schema: Optional[dict] = Field(None, description="Output schema")
    auth_required: bool = Field(False, description="Whether authentication is required")
    permission_level: str = Field("read", description="Permission level")
    risk_level: Optional[str] = Field(None, description="Risk level")
    requires_approval: bool = Field(False, description="Whether approval is required")


class ToolResponse(BaseModel):
    """Tool response schema.

    Args:
        id: Tool ID
        name: Tool name
        slug: Tool slug
        description: Tool description
        category: Tool category
        implementation_type: Implementation type
        endpoint_url: API endpoint URL
        endpoint_method: API endpoint method
        input_schema: Input schema
        output_schema: Output schema
        auth_required: Whether authentication is required
        permission_level: Permission level
        risk_level: Risk level
        requires_approval: Whether approval is required
        status: Tool status
        is_active: Whether tool is active
        created_at: Creation timestamp
        updated_at: Last update timestamp
    """

    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    category: str
    implementation_type: str
    endpoint_url: Optional[str] = None
    endpoint_method: Optional[str] = None
    input_schema: Optional[dict] = None
    output_schema: Optional[dict] = None
    auth_required: bool
    permission_level: str
    risk_level: Optional[str] = None
    requires_approval: bool
    status: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
