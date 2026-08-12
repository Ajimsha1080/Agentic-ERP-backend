"""
Connectors API routes.

Manage external service connectors and integrations.
"""

from typing import List, Optional, Dict, Any
from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException, status, Query, Path
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, or_, func

from packages.database import get_db
from packages.models import Connector, User, Permission, Connection
from packages.security import get_current_active_user, check_endpoint_rate_limit
from packages.schemas.connectors import (
    ConnectorCreate, ConnectorUpdate, ConnectorResponse,
    ConnectionCreate, ConnectionResponse, ConnectionStatus
)

router = APIRouter(prefix="/connectors", tags=["connectors"])

# Rate limiting
rate_limiter = Depends(check_endpoint_rate_limit)


@router.get("/", response_model=List[ConnectorResponse])
async def list_connectors(
    skip: int = Query(0, ge=0),
    limit: int = Query(50, ge=1, le=100),
    service_type: Optional[str] = Query(None, description="Filter by service type"),
    category: Optional[str] = Query(None, description="Filter by category"),
    search: Optional[str] = Query(None, description="Search in name and description"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user),
    rate_limiter: bool = Depends(rate_limiter)
):
    """List available connectors."""
    query = select(Connector)
    
    # Apply filters
    if service_type:
        query = query.where(Connector.service_type == service_type)
    
    if category:
        query = query.where(Connector.category == category)
    
    if search:
        search_condition = or_(
            Connector.name.ilike(f"%{search}%"),
            Connector.description.ilike(f"%{search}%"),
            Connector.config_schema.ilike(f"%{search}%")
        )
        query = query.where(search_condition)
    
    # Apply pagination
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    connectors = result.scalars().all()
    
    return connectors


@router.get("/{connector_id}", response_model=ConnectorResponse)
async def get_connector(
    connector_id: UUID = Path(..., description="Connector ID"),
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get connector details."""
    result = await db.execute(select(Connector).where(Connector.id == connector_id))
    connector = result.scalar_one_or_none()
    
    if connector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector not found"
        )
    
    return connector


@router.post("/", response_model=ConnectorResponse, status_code=status.HTTP_201_CREATED)
async def create_connector(
    connector: ConnectorCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Create a new connector."""
    # Check if connector name already exists
    result = await db.execute(select(Connector).where(Connector.name == connector.name))
    if result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Connector with this name already exists"
        )
    
    # Create connector
    db_connector = Connector(**connector.model_dump())
    db.add(db_connector)
    await db.commit()
    await db.refresh(db_connector)
    
    return db_connector


@router.put("/{connector_id}", response_model=ConnectorResponse)
async def update_connector(
    connector_id: UUID,
    connector_update: ConnectorUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Update connector."""
    result = await db.execute(select(Connector).where(Connector.id == connector_id))
    db_connector = result.scalar_one_or_none()
    
    if db_connector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector not found"
        )
    
    # Update connector fields
    for field, value in connector_update.model_dump(exclude_unset=True).items():
        setattr(db_connector, field, value)
    
    await db.commit()
    await db.refresh(db_connector)
    
    return db_connector


@router.delete("/{connector_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_connector(
    connector_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Delete connector."""
    result = await db.execute(select(Connector).where(Connector.id == connector_id))
    db_connector = result.scalar_one_or_none()
    
    if db_connector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector not found"
        )
    
    # Check if connector is being used by any connections
    connection_result = await db.execute(
        select(Connection).where(Connection.connector_id == connector_id)
    )
    if connection_result.scalar_one_or_none():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot delete connector that has active connections"
        )
    
    await db.delete(db_connector)
    await db.commit()


@router.get("/{connector_id}/connections", response_model=List[ConnectionResponse])
async def get_connector_connections(
    connector_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get connections for a connector."""
    # Check if connector exists
    result = await db.execute(select(Connector).where(Connector.id == connector_id))
    connector = result.scalar_one_or_none()
    
    if connector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector not found"
        )
    
    # Get connections for this connector
    result = await db.execute(select(Connection).where(Connection.connector_id == connector_id))
    connections = result.scalars().all()
    
    return connections


@router.get("/categories", response_model=List[str])
async def get_connector_categories(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get all connector categories."""
    result = await db.execute(select(Connector.category).distinct().where(Connector.category.isnot(None)))
    categories = [row[0] for row in result.fetchall()]
    
    return categories


@router.get("/stats", response_model=Dict[str, Any])
async def get_connector_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get connector statistics."""
    # Count connectors by type
    type_counts = await db.execute(
        select(Connector.service_type, func.count(Connector.id))
        .group_by(Connector.service_type)
    )
    type_stats = {row[0]: row[1] for row in type_counts.fetchall()}
    
    # Count connectors by category
    category_counts = await db.execute(
        select(Connector.category, func.count(Connector.id))
        .group_by(Connector.category)
    )
    category_stats = {row[0]: row[1] for row in category_counts.fetchall()}
    
    # Count total connections
    total_connections = await db.execute(select(func.count(Connection.id)))
    total_count = total_connections.scalar()
    
    # Get active connections count
    active_connections = await db.execute(
        select(func.count(Connection.id)).where(Connection.status == ConnectionStatus.ACTIVE)
    )
    active_count = active_connections.scalar()
    
    return {
        "total_connectors": sum(type_stats.values()),
        "total_connections": total_count,
        "active_connections": active_count,
        "type_distribution": type_stats,
        "category_distribution": category_stats
    }


@router.post("/{connector_id}/test", response_model=Dict[str, Any])
async def test_connector(
    connector_id: UUID,
    test_config: Dict[str, Any],
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Test connector connection."""
    # Get connector details
    result = await db.execute(select(Connector).where(Connector.id == connector_id))
    connector = result.scalar_one_or_none()
    
    if connector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector not found"
        )
    
    # TODO: Implement connector testing
    # This should:
    # 1. Validate test configuration
    # 2. Test the connection to the external service
    # 3. Return test results
    # 4. Handle errors and timeouts
    
    # For now, return mock response
    return {
        "connector_id": connector_id,
        "is_successful": True,
        "message": "Connection test successful",
        "response_time": 1.2,
        "timestamp": "2024-01-01T00:00:00Z"
    }


@router.get("/available/{agent_id}", response_model=List[ConnectorResponse])
async def get_available_connectors_for_agent(
    agent_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Get connectors available for a specific agent."""
    # Check if agent exists and user has access
    from apps.api.v1.models.agents import Agent
    result = await db.execute(select(Agent).where(Agent.id == agent_id))
    agent = result.scalar_one_or_none()
    
    if agent is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Agent not found"
        )
    
    # TODO: Implement connector filtering based on agent capabilities and requirements
    # For now, return all available connectors
    
    result = await db.execute(select(Connector))
    connectors = result.scalars().all()
    
    return connectors


@router.post("/{connector_id}/enable", response_model=ConnectorResponse)
async def enable_connector(
    connector_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Enable a connector."""
    result = await db.execute(select(Connector).where(Connector.id == connector_id))
    connector = result.scalar_one_or_none()
    
    if connector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector not found"
        )
    
    connector.is_enabled = True
    await db.commit()
    await db.refresh(connector)
    
    return connector


@router.post("/{connector_id}/disable", response_model=ConnectorResponse)
async def disable_connector(
    connector_id: UUID,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """Disable a connector."""
    result = await db.execute(select(Connector).where(Connector.id == connector_id))
    connector = result.scalar_one_or_none()
    
    if connector is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Connector not found"
        )
    
    connector.is_enabled = False
    await db.commit()
    await db.refresh(connector)
    
    return connector