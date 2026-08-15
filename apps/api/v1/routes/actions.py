"""Action routes."""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update
from typing import List, Optional

from packages.database import get_db
from packages.models import Action, Approval
from ..schemas.action import (
    ActionCreate, ActionUpdate, ActionResponse,
    ActionCreateResponse, ActionApprove, ActionReject, ActionExecute,
    WorkflowCreate, WorkflowResponse, ApprovalRequestCreate, ApprovalRequestResponse
)
from ..schemas.base import PaginatedResponse
from packages.security.auth import get_current_user

router = APIRouter(prefix="/actions", tags=["Actions"])


@router.get("", response_model=PaginatedResponse[ActionResponse])
async def list_actions(
    page: int = 1,
    page_size: int = 20,
    action_type: Optional[str] = None,
    status: Optional[str] = None,
    agent_id: Optional[str] = None,
    organization_id: Optional[str] = None,
    requested_by_id: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List actions.

    Args:
        page: Page number
        page_size: Items per page
        action_type: Filter by action type
        status: Filter by status
        agent_id: Filter by agent ID
        organization_id: Filter by organization ID
        requested_by_id: Filter by user ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        PaginatedResponse: Paginated list of actions
    """
    # Build query
    query = select(Action)

    # Filter by action type
    if action_type:
        query = query.where(Action.action_type == action_type)

    # Filter by status
    if status:
        query = query.where(Action.status == status)

    # Filter by agent
    if agent_id:
        query = query.where(Action.agent_id == UUID(agent_id))

    # Filter by organization
    if organization_id:
        query = query.where(Action.organization_id == UUID(organization_id))

    # Filter by user
    if requested_by_id:
        query = query.where(Action.requested_by_id == UUID(requested_by_id))

    # Get total count
    count_query = select(Action).union_all(query)
    total_result = await db.execute(count_query)
    total = len(total_result.all())

    # Apply pagination
    offset = (page - 1) * page_size
    query = query.offset(offset).limit(page_size)

    # Execute
    result = await db.execute(query)
    actions = result.scalars().all()

    return {
        "items": actions,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": (total + page_size - 1) // page_size
    }


@router.get("/{action_id}", response_model=ActionResponse)
async def get_action(
    action_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get action by ID.

    Args:
        action_id: Action ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        ActionResponse: Action information

    Raises:
        HTTPException: If action not found
    """
    result = await db.execute(
        select(Action).where(Action.id == UUID(action_id))
    )
    action = result.scalar_one_or_none()

    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )

    return action


@router.post("", response_model=ActionCreateResponse, status_code=status.HTTP_201_CREATED)
async def create_action(
    action_data: ActionCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Create a new action.

    Args:
        action_data: Action creation data
        db: Database session
        current_user: Current authenticated user

    Returns:
        ActionCreateResponse: Created action with ID

    Raises:
        HTTPException: If action creation fails
    """
    # Create action
    action = Action(
        action_type=action_data.action_type,
        name=action_data.name,
        description=action_data.description,
        agent_execution_id=action_data.agent_execution_id,
        requested_by_id=action_data.requested_by_id,
        action_data=action_data.action_data,
        status="proposed",
        proposed_at=datetime.utcnow(),
        created_by_id=current_user.id
    )

    db.add(action)
    await db.commit()
    await db.refresh(action)

    return {
        "id": action.id,
        "action": action
    }


@router.put("/{action_id}", response_model=ActionResponse)
async def update_action(
    action_id: str,
    action_data: ActionUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Update action.

    Args:
        action_id: Action ID
        action_data: Action update data
        db: Database session
        current_user: Current authenticated user

    Returns:
        ActionResponse: Updated action

    Raises:
        HTTPException: If action not found or update fails
    """
    result = await db.execute(
        select(Action).where(Action.id == UUID(action_id))
    )
    action = result.scalar_one_or_none()

    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )

    # Update fields
    update_data = action_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(action, field, value)

    # Update timestamp
    action.updated_at = datetime.utcnow()

    await db.commit()
    await db.refresh(action)

    return action


@router.delete("/{action_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_action(
    action_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Delete action.

    Args:
        action_id: Action ID
        db: Database session
        current_user: Current authenticated user

    Raises:
        HTTPException: If action not found or deletion fails
    """
    result = await db.execute(
        select(Action).where(Action.id == UUID(action_id))
    )
    action = result.scalar_one_or_none()

    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )

    await db.delete(action)
    await db.commit()

    return None


@router.post("/{action_id}/approve", status_code=status.HTTP_200_OK)
async def approve_action(
    action_id: str,
    approval_data: ActionApprove,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Approve action.

    Args:
        action_id: Action ID
        approval_data: Approval data
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Success message

    Raises:
        HTTPException: If action not found or approval fails
    """
    # Get action
    result = await db.execute(
        select(Action).where(Action.id == UUID(action_id))
    )
    action = result.scalar_one_or_none()

    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )

    # Check if action is pending approval
    if action.status != "approval_required":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Action is not pending approval. Current status: {action.status}"
        )

    # Create approval
    approval = Approval(
        action_id=UUID(action_id),
        approver_id=current_user.id,
        status=approval_data.action_on_action,
        comments=approval_data.comments
    )

    db.add(approval)
    await db.commit()

    return {"message": f"Action {approval_data.action_on_action} successfully"}


@router.post("/{action_id}/reject", status_code=status.HTTP_200_OK)
async def reject_action(
    action_id: str,
    rejection_data: ActionReject,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Reject action.

    Args:
        action_id: Action ID
        rejection_data: Rejection data
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Success message

    Raises:
        HTTPException: If action not found or rejection fails
    """
    # Get action
    result = await db.execute(
        select(Action).where(Action.id == UUID(action_id))
    )
    action = result.scalar_one_or_none()

    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )

    # Create rejection (as approval)
    approval = Approval(
        action_id=UUID(action_id),
        approver_id=current_user.id,
        status="rejected",
        comments=f"Rejected: {rejection_data.rejection_reason}\n{rejection_data.comments}"
    )

    db.add(approval)
    await db.commit()

    return {"message": "Action rejected successfully"}


@router.get("/{action_id}/approvals", response_model=List[ApprovalRequestResponse])
async def get_action_approvals(
    action_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Get action approvals.

    Args:
        action_id: Action ID
        db: Database session
        current_user: Current authenticated user

    Returns:
        List[ApprovalRequestResponse]: List of approvals
    """
    # Get approvals
    result = await db.execute(
        select(Approval).where(Approval.action_id == UUID(action_id))
    )
    approvals = result.scalars().all()

    # Convert to response
    approval_responses = []
    for approval in approvals:
        approval_responses.append(ApprovalRequestResponse(
            id=approval.id,
            action_id=approval.action_id,
            approver_id=approval.approver_id,
            approver_role_id=approval.approver_role_id,
            status=approval.status,
            justification=approval.justification,
            approval_type=approval.approval_type,
            approver_sequence=approval.approver_sequence,
            delegated_to_id=approval.delegated_to_id,
            requested_at=approval.requested_at,
            approved_at=approval.approved_at
        ))

    return approval_responses


@router.post("/{action_id}/execute", status_code=status.HTTP_200_OK)
async def execute_action(
    action_id: str,
    execution_data: ActionExecute,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """Execute action.

    Args:
        action_id: Action ID
        execution_data: Execution data
        db: Database session
        current_user: Current authenticated user

    Returns:
        dict: Success message

    Raises:
        HTTPException: If action not found or execution fails
    """
    # Get action
    result = await db.execute(
        select(Action).where(Action.id == UUID(action_id))
    )
    action = result.scalar_one_or_none()

    if not action:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Action not found"
        )

    # Check if action is approved
    if action.status != "approved":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Action must be approved before execution. Current status: {action.status}"
        )

    # TODO: Implement actual action execution
    # This requires:
    # 1. Loading action data
    # 2. Validating action parameters
    # 3. Calling appropriate tool
    # 4. Handling tool response
    # 5. Updating action status
    # 6. Recording execution logs
    # 7. Triggering verification

    # For now, mark as executing
    action.status = "executing"
    action.executed_at = datetime.utcnow()
    action.execution_result = {"message": "Action execution not yet implemented"}

    await db.commit()

    return {"message": "Action execution started. Implementation pending."}


@router.get("/types", response_model=List[str])
async def list_action_types(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """List all action types.

    Args:
        db: Database session
        current_user: Current authenticated user

    Returns:
        List[str]: List of action types
    """
    # Get all unique types
    result = await db.execute(select(Action.action_type).distinct())
    types = result.scalars().all()

    return list(types)
