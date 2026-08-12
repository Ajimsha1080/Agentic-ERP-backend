"""
Data tasks.

Background tasks for data processing and analytics.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
import asyncio
import json

from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, func, desc, asc

from packages.database import get_async_db_session
from packages.models import (
    ToolExecution, WorkflowExecution, AgentExecution, 
    UserActivityLog, SystemLog, Agent, Workflow, Tool, User
)
from packages.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@shared_task(bind=True, name="data.generate_system_metrics")
async def generate_system_metrics_task(
    self,
    days: int = 7,
    include_realtime: bool = True
) -> Dict[str, Any]:
    """Generate system metrics and analytics asynchronously.
    
    Args:
        days: Number of days to analyze
        include_realtime: Whether to include real-time metrics
        
    Returns:
        Dict: Metrics results
    """
    start_time = datetime.utcnow()
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            metrics_results = {
                "status": "completed",
                "analysis_time": (datetime.utcnow() - start_time).total_seconds(),
                "days_analyzed": days,
                "generated_at": datetime.utcnow().isoformat(),
                "metrics": {}
            }
            
            # System Overview Metrics
            metrics_results["metrics"]["overview"] = {
                "total_executions": 0,
                "active_users": 0,
                "active_agents": 0,
                "active_workflows": 0,
                "total_tools": 0,
                "system_uptime": "99.9%"
            }
            
            # Calculate total executions
            executions_query = select(
                func.count(ToolExecution.id) + 
                func.count(WorkflowExecution.id) + 
                func.count(AgentExecution.id)
            ).where(
                ToolExecution.created_at >= cutoff_date,
                WorkflowExecution.created_at >= cutoff_date,
                AgentExecution.created_at >= cutoff_date
            )
            executions_result = await db_session.execute(executions_query)
            total_executions = executions_result.scalar() or 0
            metrics_results["metrics"]["overview"]["total_executions"] = total_executions
            
            # Calculate active users
            active_users_query = select(func.count(User.id)).where(
                and_(
                    User.last_login >= cutoff_date,
                    User.is_active == True
                )
            )
            active_users_result = await db_session.execute(active_users_query)
            active_users = active_users_result.scalar() or 0
            metrics_results["metrics"]["overview"]["active_users"] = active_users
            
            # Calculate active agents
            active_agents_query = select(func.count(Agent.id)).where(
                and_(
                    Agent.is_active == True,
                    Agent.updated_at >= cutoff_date
                )
            )
            active_agents_result = await db_session.execute(active_agents_query)
            active_agents = active_agents_result.scalar() or 0
            metrics_results["metrics"]["overview"]["active_agents"] = active_agents
            
            # Calculate active workflows
            active_workflows_query = select(func.count(Workflow.id)).where(
                and_(
                    Workflow.status == "active",
                    Workflow.updated_at >= cutoff_date
                )
            )
            active_workflows_result = await db_session.execute(active_workflows_query)
            active_workflows = active_workflows_result.scalar() or 0
            metrics_results["metrics"]["overview"]["active_workflows"] = active_workflows
            
            # Calculate total tools
            total_tools_query = select(func.count(Tool.id)).where(Tool.is_active == True)
            total_tools_result = await db_session.execute(total_tools_query)
            total_tools = total_tools_result.scalar() or 0
            metrics_results["metrics"]["overview"]["total_tools"] = total_tools
            
            # Execution Metrics
            metrics_results["metrics"]["executions"] = {
                "tool_executions": await _get_tool_execution_metrics(db_session, cutoff_date),
                "workflow_executions": await _get_workflow_execution_metrics(db_session, cutoff_date),
                "agent_executions": await _get_agent_execution_metrics(db_session, cutoff_date),
                "execution_trends": await _get_execution_trends(db_session, cutoff_date)
            }
            
            # Performance Metrics
            metrics_results["metrics"]["performance"] = {
                "average_execution_time": await _get_average_execution_time(db_session, cutoff_date),
                "success_rate": await _get_success_rate(db_session, cutoff_date),
                "concurrent_executions": await _get_concurrent_executions(db_session),
                "error_rate": await _get_error_rate(db_session, cutoff_date)
            }
            
            # User Activity Metrics
            metrics_results["metrics"]["user_activity"] = {
                "daily_active_users": await _get_daily_active_users(db_session, cutoff_date),
                "user_sessions": await _get_user_sessions(db_session, cutoff_date),
                "top_users": await _get_top_users(db_session, cutoff_date)
            }
            
            # Agent Performance Metrics
            metrics_results["metrics"]["agent_performance"] = {
                "agent_usage": await _get_agent_usage_metrics(db_session, cutoff_date),
                "agent_success_rates": await _get_agent_success_rates(db_session, cutoff_date),
                "agent_execution_times": await _get_agent_execution_times(db_session, cutoff_date)
            }
            
            # Real-time metrics (if requested)
            if include_realtime:
                metrics_results["metrics"]["realtime"] = await _get_realtime_metrics(db_session)
            
            await db_session.commit()
            
            logger.info(f"System metrics generated for {days} days")
            
            return metrics_results
            
    except Exception as e:
        logger.error(f"Error generating system metrics: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "analysis_time": (datetime.utcnow() - start_time).total_seconds()
        }


async def _get_tool_execution_metrics(db_session: AsyncSession, cutoff_date: datetime) -> Dict[str, Any]:
    """Get tool execution metrics."""
    query = select(
        Tool.name,
        func.count(ToolExecution.id).label("count"),
        func.avg(ToolExecution.execution_time).label("avg_time"),
        func.max(ToolExecution.execution_time).label("max_time"),
        func.min(ToolExecution.execution_time).label("min_time")
    ).join(
        ToolExecution,
        Tool.id == ToolExecution.tool_id
    ).where(
        ToolExecution.created_at >= cutoff_date
    ).group_by(
        Tool.name
    ).order_by(
        func.count(ToolExecution.id).desc()
    ).limit(10)
    
    result = await db_session.execute(query)
    return [{"name": row.name, "count": row.count, "avg_time": row.avg_time, "max_time": row.max_time, "min_time": row.min_time} for row in result]


async def _get_workflow_execution_metrics(db_session: AsyncSession, cutoff_date: datetime) -> Dict[str, Any]:
    """Get workflow execution metrics."""
    query = select(
        Workflow.name,
        func.count(WorkflowExecution.id).label("count"),
        func.avg(WorkflowExecution.execution_time).label("avg_time"),
        func.sum(WorkflowExecution.input_data).label("total_input_size"),
        func.sum(WorkflowExecution.output_data).label("total_output_size")
    ).join(
        WorkflowExecution,
        Workflow.id == WorkflowExecution.workflow_id
    ).where(
        WorkflowExecution.created_at >= cutoff_date
    ).group_by(
        Workflow.name
    ).order_by(
        func.count(WorkflowExecution.id).desc()
    ).limit(10)
    
    result = await db_session.execute(query)
    return [{"name": row.name, "count": row.count, "avg_time": row.avg_time, "total_input_size": row.total_input_size, "total_output_size": row.total_output_size} for row in result]


async def _get_agent_execution_metrics(db_session: AsyncSession, cutoff_date: datetime) -> Dict[str, Any]:
    """Get agent execution metrics."""
    query = select(
        Agent.name,
        func.count(AgentExecution.id).label("count"),
        func.avg(AgentExecution.execution_time).label("avg_time"),
        func.sum(AgentExecution.steps_completed).label("total_steps"),
        func.sum(AgentExecution.actions_taken).label("total_actions")
    ).join(
        AgentExecution,
        Agent.id == AgentExecution.agent_id
    ).where(
        AgentExecution.created_at >= cutoff_date
    ).group_by(
        Agent.name
    ).order_by(
        func.count(AgentExecution.id).desc()
    ).limit(10)
    
    result = await db_session.execute(query)
    return [{"name": row.name, "count": row.count, "avg_time": row.avg_time, "total_steps": row.total_steps, "total_actions": row.total_actions} for row in result]


async def _get_execution_trends(db_session: AsyncSession, cutoff_date: datetime) -> List[Dict[str, Any]]:
    """Get execution trends over time."""
    query = select(
        func.date(ToolExecution.created_at).label("date"),
        func.count(ToolExecution.id).label("tool_count"),
        func.count(WorkflowExecution.id).label("workflow_count"),
        func.count(AgentExecution.id).label("agent_count")
    ).where(
        ToolExecution.created_at >= cutoff_date,
        WorkflowExecution.created_at >= cutoff_date,
        AgentExecution.created_at >= cutoff_date
    ).group_by(
        func.date(ToolExecution.created_at)
    ).order_by(
        func.date(ToolExecution.created_at)
    )
    
    result = await db_session.execute(query)
    return [{"date": row.date.isoformat(), "tool_count": row.tool_count, "workflow_count": row.workflow_count, "agent_count": row.agent_count} for row in result]


async def _get_average_execution_time(db_session: AsyncSession, cutoff_date: datetime) -> float:
    """Get average execution time."""
    query = select(
        (func.avg(ToolExecution.execution_time) + 
         func.avg(WorkflowExecution.execution_time) + 
         func.avg(AgentExecution.execution_time)) / 3
    ).where(
        ToolExecution.created_at >= cutoff_date,
        WorkflowExecution.created_at >= cutoff_date,
        AgentExecution.created_at >= cutoff_date
    )
    
    result = await db_session.execute(query)
    return result.scalar() or 0.0


async def _get_success_rate(db_session: AsyncSession, cutoff_date: datetime) -> float:
    """Get success rate for executions."""
    from packages.models import ToolExecution, WorkflowExecution, AgentExecution
    
    total_query = select(
        func.count(ToolExecution.id) + 
        func.count(WorkflowExecution.id) + 
        func.count(AgentExecution.id)
    ).where(
        ToolExecution.created_at >= cutoff_date,
        WorkflowExecution.created_at >= cutoff_date,
        AgentExecution.created_at >= cutoff_date
    )
    
    success_query = select(
        func.sum(case([(ToolExecution.status == "completed", 1)], else_=0)) +
        func.sum(case([(WorkflowExecution.status == "completed", 1)], else_=0)) +
        func.sum(case([(AgentExecution.status == "completed", 1)], else_=0))
    ).where(
        ToolExecution.created_at >= cutoff_date,
        WorkflowExecution.created_at >= cutoff_date,
        AgentExecution.created_at >= cutoff_date
    )
    
    total_result = await db_session.execute(total_query)
    total_count = total_result.scalar() or 0
    
    success_result = await db_session.execute(success_query)
    success_count = success_result.scalar() or 0
    
    return (success_count / total_count * 100) if total_count > 0 else 0.0


async def _get_error_rate(db_session: AsyncSession, cutoff_date: datetime) -> float:
    """Get error rate for executions."""
    from packages.models import ToolExecution, WorkflowExecution, AgentExecution
    
    error_query = select(
        func.sum(case([(ToolExecution.status == "failed", 1)], else_=0)) +
        func.sum(case([(WorkflowExecution.status == "failed", 1)], else_=0)) +
        func.sum(case([(AgentExecution.status == "failed", 1)], else_=0))
    ).where(
        ToolExecution.created_at >= cutoff_date,
        WorkflowExecution.created_at >= cutoff_date,
        AgentExecution.created_at >= cutoff_date
    )
    
    total_query = select(
        func.count(ToolExecution.id) + 
        func.count(WorkflowExecution.id) + 
        func.count(AgentExecution.id)
    ).where(
        ToolExecution.created_at >= cutoff_date,
        WorkflowExecution.created_at >= cutoff_date,
        AgentExecution.created_at >= cutoff_date
    )
    
    error_result = await db_session.execute(error_query)
    error_count = error_result.scalar() or 0
    
    total_result = await db_session.execute(total_query)
    total_count = total_result.scalar() or 0
    
    return (error_count / total_count * 100) if total_count > 0 else 0.0


async def _get_concurrent_executions(db_session: AsyncSession) -> int:
    """Get number of concurrent executions."""
    from packages.models import ToolExecution, WorkflowExecution, AgentExecution
    
    query = select(
        func.count(ToolExecution.id).label("tool_count") +
        func.count(WorkflowExecution.id).label("workflow_count") +
        func.count(AgentExecution.id).label("agent_count")
    ).where(
        ToolExecution.status == "running",
        WorkflowExecution.status == "running",
        AgentExecution.status == "running"
    )
    
    result = await db_session.execute(query)
    return result.scalar() or 0


async def _get_daily_active_users(db_session: AsyncSession, cutoff_date: datetime) -> List[Dict[str, Any]]:
    """Get daily active users."""
    query = select(
        func.date(UserActivityLog.created_at).label("date"),
        func.count(func.distinct(UserActivityLog.user_id)).label("active_users")
    ).where(
        UserActivityLog.created_at >= cutoff_date
    ).group_by(
        func.date(UserActivityLog.created_at)
    ).order_by(
        func.date(UserActivityLog.created_at)
    )
    
    result = await db_session.execute(query)
    return [{"date": row.date.isoformat(), "active_users": row.active_users} for row in result]


async def _get_user_sessions(db_session: AsyncSession, cutoff_date: datetime) -> Dict[str, Any]:
    """Get user session statistics."""
    query = select(
        func.count(UserActivityLog.id).label("total_sessions"),
        func.avg(func.datediff(UserActivityLog.updated_at, UserActivityLog.created_at)).label("avg_session_duration")
    ).where(
        UserActivityLog.created_at >= cutoff_date
    )
    
    result = await db_session.execute(query)
    return {"total_sessions": result.scalar()[0] or 0, "avg_session_duration": result.scalar()[1] or 0}


async def _get_top_users(db_session: AsyncSession, cutoff_date: datetime) -> List[Dict[str, Any]]:
    """Get top active users."""
    query = select(
        User.username,
        func.count(UserActivityLog.id).label("activity_count"),
        func.max(UserActivityLog.created_at).label("last_activity")
    ).join(
        UserActivityLog,
        User.id == UserActivityLog.user_id
    ).where(
        UserActivityLog.created_at >= cutoff_date
    ).group_by(
        User.id,
        User.username
    ).order_by(
        func.count(UserActivityLog.id).desc()
    ).limit(10)
    
    result = await db_session.execute(query)
    return [{"username": row.username, "activity_count": row.activity_count, "last_activity": row.last_activity.isoformat()} for row in result]


async def _get_agent_usage_metrics(db_session: AsyncSession, cutoff_date: datetime) -> List[Dict[str, Any]]:
    """Get agent usage metrics."""
    query = select(
        Agent.name,
        func.count(AgentExecution.id).label("usage_count"),
        func.max(AgentExecution.created_at).label("last_used")
    ).join(
        AgentExecution,
        Agent.id == AgentExecution.agent_id
    ).where(
        AgentExecution.created_at >= cutoff_date
    ).group_by(
        Agent.id,
        Agent.name
    ).order_by(
        func.count(AgentExecution.id).desc()
    ).limit(10)
    
    result = await db_session.execute(query)
    return [{"name": row.name, "usage_count": row.usage_count, "last_used": row.last_used.isoformat()} for row in result]


async def _get_agent_success_rates(db_session: AsyncSession, cutoff_date: datetime) -> List[Dict[str, Any]]:
    """Get agent success rates."""
    query = select(
        Agent.name,
        func.count(AgentExecution.id).label("total_executions"),
        func.sum(case([(AgentExecution.status == "completed", 1)], else_=0)).label("successful_executions"),
        func.avg(AgentExecution.execution_time).label("avg_execution_time")
    ).join(
        AgentExecution,
        Agent.id == AgentExecution.agent_id
    ).where(
        AgentExecution.created_at >= cutoff_date
    ).group_by(
        Agent.id,
        Agent.name
    ).order_by(
        func.count(AgentExecution.id).desc()
    ).limit(10)
    
    result = await db_session.execute(query)
    return [
        {
            "name": row.name, 
            "success_rate": (row.successful_executions / row.total_executions * 100) if row.total_executions > 0 else 0,
            "avg_execution_time": row.avg_execution_time or 0
        } 
        for row in result
    ]


async def _get_agent_execution_times(db_session: AsyncSession, cutoff_date: datetime) -> List[Dict[str, Any]]:
    """Get agent execution time distribution."""
    query = select(
        Agent.name,
        func.avg(AgentExecution.execution_time).label("avg_time"),
        func.min(AgentExecution.execution_time).label("min_time"),
        func.max(AgentExecution.execution_time).label("max_time")
    ).join(
        AgentExecution,
        Agent.id == AgentExecution.agent_id
    ).where(
        AgentExecution.created_at >= cutoff_date
    ).group_by(
        Agent.id,
        Agent.name
    ).order_by(
        func.avg(AgentExecution.execution_time).desc()
    ).limit(10)
    
    result = await db_session.execute(query)
    return [{"name": row.name, "avg_time": row.avg_time, "min_time": row.min_time, "max_time": row.max_time} for row in result]


async def _get_realtime_metrics(db_session: AsyncSession) -> Dict[str, Any]:
    """Get real-time metrics."""
    return {
        "concurrent_executions": await _get_concurrent_executions(db_session),
        "active_users": await db_session.execute(
            select(func.count(User.id)).where(
                and_(
                    User.is_active == True,
                    User.last_login >= datetime.utcnow() - timedelta(hours=1)
                )
            )
        ).scalar() or 0,
        "memory_usage": "85%",  # Mock real-time memory usage
        "cpu_usage": "65%",     # Mock real-time CPU usage
        "disk_usage": "45%"      # Mock real-time disk usage
    }