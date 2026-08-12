"""Action-related schemas."""

from typing import Optional, List
from pydantic import BaseModel, Field, HttpUrl
from datetime import datetime
from uuid import UUID

from .base import UUIDResponse, PaginationParams, PaginatedResponse


class ActionCreate(BaseModel):
    """Action creation schema.

    Args:
        action_type: Action type
        name: Action name
        description: Action description
        agent_execution_id: Agent execution ID
        requested_by_id: User ID requesting the action
        action_data: Action data (parameters)
    """

    action_type: str = Field(..., description="Action type")
    name: str = Field(..., min_length=1, max_length=255, description="Action name")
    description: Optional[str] = Field(None, description="Action description")
    agent_execution_id: Optional[UUID] = Field(None, description="Agent execution ID")
    requested_by_id: Optional[UUID] = Field(None, description="User ID requesting the action")
    action_data: Optional[dict] = Field(None, description="Action data")


class ActionUpdate(BaseModel):
    """Action update schema.

    Args:
        name: Action name
        description: Action description
    """

    name: Optional[str] = Field(None, min_length=1, max_length=255)
    description: Optional[str] = None


class ActionResponse(BaseModel):
    """Action response schema.

    Args:
        id: Action ID
        action_type: Action type
        name: Action name
        description: Action description
        status: Action status
        agent_execution_id: Agent execution ID
        agent_id: Agent ID
        requested_by_id: User ID
        action_data: Action data
        policy_compliant: Whether action is policy compliant
        requires_approval: Whether approval is required
        is_verified: Whether action is verified
        proposed_at: Proposed timestamp
        approved_at: Approved timestamp
        approved_by_id: Approved by user ID
        executed_at: Executed timestamp
        verified_at: Verified timestamp
        estimated_cost: Estimated cost
        actual_cost: Actual cost
        idempotency_key: Idempotency key
        created_at: Creation timestamp
    """

    id: UUID
    action_type: str
    name: str
    description: Optional[str] = None
    status: str
    agent_execution_id: Optional[UUID] = None
    agent_id: Optional[UUID] = None
    requested_by_id: Optional[UUID] = None
    action_data: Optional[dict] = None
    policy_compliant: bool
    requires_approval: bool
    is_verified: bool
    proposed_at: datetime
    approved_at: Optional[datetime] = None
    approved_by_id: Optional[UUID] = None
    executed_at: Optional[datetime] = None
    verified_at: Optional[datetime] = None
    estimated_cost: Optional[float] = None
    actual_cost: Optional[float] = None
    idempotency_key: Optional[str] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)


class ActionCreateResponse(UUIDResponse):
    """Action creation response.

    Inherits from UUIDResponse.
    """

    action: ActionResponse


class ApprovalRequestCreate(BaseModel):
    """Approval request creation schema.

    Args:
        action_id: Action ID
        approver_id: Approver user ID
        approver_role_id: Approver role ID
        justification: Approval justification
        approval_type: Approval type
    """

    action_id: UUID = Field(..., description="Action ID")
    approver_id: Optional[UUID] = Field(None, description="Approver user ID")
    approver_role_id: Optional[UUID] = Field(None, description="Approver role ID")
    justification: Optional[str] = Field(None, description="Approval justification")
    approval_type: Optional[str] = Field(None, description="Approval type")


class ApprovalRequestResponse(BaseModel):
    """Approval request response schema.

    Args:
        id: Request ID
        action_id: Action ID
        approver_id: Approver user ID
        approver_role_id: Approver role ID
        status: Request status
        justification: Justification
        approval_type: Approval type
        approver_sequence: Approver sequence
        delegated_to_id: Delegated to user ID
        requested_at: Requested timestamp
        approved_at: Approved timestamp
    """

    id: UUID
    action_id: UUID
    approver_id: Optional[UUID] = None
    approver_role_id: Optional[UUID] = None
    status: str
    justification: Optional[str] = None
    approval_type: Optional[str] = None
    approver_sequence: Optional[int] = None
    delegated_to_id: Optional[UUID] = None
    requested_at: datetime
    approved_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ActionApprove(BaseModel):
    """Action approval schema.

    Args:
        approval_id: Approval request ID
        comments: Approval comments
        action_on_action: Action to take (approve, reject, request_changes)
    """

    approval_id: UUID = Field(..., description="Approval request ID")
    comments: Optional[str] = Field(None, description="Approval comments")
    action_on_action: str = Field("approve", description="Action to take: approve, reject, request_changes")


class ActionReject(BaseModel):
    """Action rejection schema.

    Args:
        rejection_reason: Rejection reason
        comments: Rejection comments
    """

    rejection_reason: str = Field(..., min_length=1, description="Rejection reason")
    comments: Optional[str] = Field(None, description="Rejection comments")


class ActionExecute(BaseModel):
    """Action execution schema.

    Args:
        action_id: Action ID
        execution_data: Additional execution data
    """

    action_id: UUID = Field(..., description="Action ID")
    execution_data: Optional[dict] = Field(None, description="Additional execution data")


class WorkflowCreate(BaseModel):
    """Workflow creation schema.

    Args:
        name: Workflow name
        slug: Workflow slug
        description: Workflow description
        type: Workflow type
        trigger_type: Trigger type
        trigger_config: Trigger configuration
    """

    name: str = Field(..., min_length=1, max_length=255, description="Workflow name")
    slug: str = Field(..., min_length=1, max_length=100, description="Workflow slug")
    description: Optional[str] = Field(None, description="Workflow description")
    type: str = Field(..., description="Workflow type")
    trigger_type: str = Field(..., description="Trigger type")
    trigger_config: Optional[dict] = Field(None, description="Trigger configuration")


class WorkflowResponse(BaseModel):
    """Workflow response schema.

    Args:
        id: Workflow ID
        name: Workflow name
        slug: Workflow slug
        description: Workflow description
        type: Workflow type
        status: Workflow status
        is_active: Whether workflow is active
        trigger_type: Trigger type
        trigger_config: Trigger configuration
        total_executions: Total executions
        successful_executions: Successful executions
        failed_executions: Failed executions
        average_duration_seconds: Average duration in seconds
        last_execution_at: Last execution timestamp
        created_at: Creation timestamp
    """

    id: UUID
    name: str
    slug: str
    description: Optional[str] = None
    type: str
    status: str
    is_active: bool
    trigger_type: str
    trigger_config: Optional[dict] = None
    total_executions: int
    successful_executions: int
    failed_executions: int
    average_duration_seconds: Optional[float] = None
    last_execution_at: Optional[datetime] = None
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
