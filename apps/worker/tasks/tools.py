"""
Tool tasks.

Background tasks for AI tool operations.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
import json

from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, func

from packages.database import get_async_db_session
from packages.models import Tool, ToolExecution
from packages.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@shared_task(bind=True, name="tool.execute_tool")
async def execute_tool_task(
    self,
    tool_id: str,
    agent_id: Optional[str] = None,
    user_id: Optional[str] = None,
    inputs: Dict[str, Any] = None,
    config: Optional[Dict[str, Any]] = None,
    timeout: Optional[int] = None
) -> Dict[str, Any]:
    """Execute a tool asynchronously.
    
    Args:
        tool_id: Tool ID
        agent_id: Optional agent ID
        user_id: Optional user ID
        inputs: Input data for the tool
        config: Optional configuration override
        timeout: Optional execution timeout in seconds
        
    Returns:
        Dict: Execution results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Get tool details
            tool_result = await db_session.execute(select(Tool).where(Tool.id == UUID(tool_id)))
            tool = tool_result.scalar_one_or_none()
            
            if not tool:
                raise ValueError(f"Tool {tool_id} not found")
            
            # Create execution record
            execution = ToolExecution(
                tool_id=UUID(tool_id),
                agent_id=UUID(agent_id) if agent_id else None,
                user_id=UUID(user_id) if user_id else None,
                input_data=inputs,
                config=config,
                status="running",
                metadata={"tool_name": tool.name}
            )
            db_session.add(execution)
            await db_session.commit()
            await db_session.refresh(execution)
            
            # Tool execution logic (mocked for now)
            
            # Simulate tool execution
            import asyncio
            await asyncio.sleep(1)  # Simulate processing time
            
            # Mock results based on tool type
            tool_output = {
                "result": f"Tool execution completed for {tool.name}",
                "execution_time": 1.0,
                "data_processed": 100,
                "steps_completed": 3
            }
            
            # Add tool-specific results
            if tool.type == "api":
                tool_output.update({
                    "api_calls": 5,
                    "response_codes": [200, 200, 200, 200, 200]
                })
            elif tool.type == "database":
                tool_output.update({
                    "queries_executed": 3,
                    "rows_processed": 150
                })
            elif tool.type == "file":
                tool_output.update({
                    "files_processed": 2,
                    "files_size": "1.5MB"
                })
            elif tool.type == "ai":
                tool_output.update({
                    "tokens_used": 500,
                    "model_used": "gpt-3.5-turbo"
                })
            
            # Update execution record
            execution.status = "completed"
            execution.completed_at = datetime.utcnow()
            execution.execution_time = (datetime.utcnow() - start_time).total_seconds()
            execution.output_data = tool_output
            
            # Update tool usage stats
            tool.usage_count += 1
            tool.last_used_at = datetime.utcnow()
            
            await db_session.commit()
            
            logger.info(f"Tool execution completed: {tool_id}")
            
            return {
                "execution_id": str(execution.id),
                "status": "completed",
                "output": tool_output,
                "execution_time": execution.execution_time,
                "tool_name": tool.name
            }
            
    except Exception as e:
        logger.error(f"Error executing tool {tool_id}: {str(e)}", exc_info=True)
        
        # Update execution record with error
        async for db_session in get_async_db_session():
            execution_result = await db_session.execute(
                select(ToolExecution).where(ToolExecution.id == execution.id)
            )
            execution = execution_result.scalar_one_or_none()
            
            if execution:
                execution.status = "failed"
                execution.completed_at = datetime.utcnow()
                execution.execution_time = (datetime.utcnow() - start_time).total_seconds()
                execution.error_message = str(e)
                await db_session.commit()
        
        return {
            "execution_id": str(execution.id) if execution else "unknown",
            "status": "failed",
            "error": str(e),
            "execution_time": (datetime.utcnow() - start_time).total_seconds()
        }


@shared_task(bind=True, name="tool.validate_tool_inputs")
async def validate_tool_inputs_task(
    self,
    tool_id: str,
    inputs: Dict[str, Any],
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Validate tool inputs asynchronously.
    
    Args:
        tool_id: Tool ID
        inputs: Input data to validate
        config: Optional configuration override
        
    Returns:
        Dict: Validation results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Get tool details
            tool_result = await db_session.execute(select(Tool).where(Tool.id == UUID(tool_id)))
            tool = tool_result.scalar_one_or_none()
            
            if not tool:
                raise ValueError(f"Tool {tool_id} not found")
            
            # Input validation logic (mocked for now)
            validation_results = {
                "is_valid": True,
                "errors": [],
                "warnings": [],
                "valid_inputs": inputs,
                "validation_time": (datetime.utcnow() - start_time).total_seconds()
            }
            
            # Simulate validation
            import random
            if random.random() < 0.1:  # 10% chance of validation failure
                validation_results.update({
                    "is_valid": False,
                    "errors": ["Input validation failed for field 'data'"]
                })
            
            logger.info(f"Tool input validation completed: {tool_id}")
            
            return validation_results
            
    except Exception as e:
        logger.error(f"Error validating tool inputs {tool_id}: {str(e)}", exc_info=True)
        return {
            "is_valid": False,
            "errors": [str(e)],
            "validation_time": (datetime.utcnow() - start_time).total_seconds()
        }


@shared_task(bind=True, name="tool.update_tool_metadata")
async def update_tool_metadata_task(
    self,
    tool_id: str,
    metadata_updates: Dict[str, Any]
) -> Dict[str, Any]:
    """Update tool metadata asynchronously.
    
    Args:
        tool_id: Tool ID
        metadata_updates: Metadata updates
        
    Returns:
        Dict: Update results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Get tool details
            tool_result = await db_session.execute(select(Tool).where(Tool.id == UUID(tool_id)))
            tool = tool_result.scalar_one_or_none()
            
            if not tool:
                raise ValueError(f"Tool {tool_id} not found")
            
            # Update metadata
            if "tags" in metadata_updates:
                tool.tags = metadata_updates["tags"]
            if "config_schema" in metadata_updates:
                tool.config_schema = metadata_updates["config_schema"]
            if "input_schema" in metadata_updates:
                tool.input_schema = metadata_updates["input_schema"]
            if "output_schema" in metadata_updates:
                tool.output_schema = metadata_updates["output_schema"]
            
            tool.updated_at = datetime.utcnow()
            await db_session.commit()
            
            logger.info(f"Tool metadata updated: {tool_id}")
            
            return {
                "status": "completed",
                "update_time": (datetime.utcnow() - start_time).total_seconds(),
                "updated_fields": list(metadata_updates.keys())
            }
            
    except Exception as e:
        logger.error(f"Error updating tool metadata {tool_id}: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "update_time": (datetime.utcnow() - start_time).total_seconds()
        }


@shared_task(bind=True, name="tool.analyze_tool_usage")
async def analyze_tool_usage_task(
    self,
    days: int = 30,
    tool_type: Optional[str] = None,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """Analyze tool usage patterns asynchronously.
    
    Args:
        days: Number of days to analyze
        tool_type: Optional tool type filter
        category: Optional category filter
        
    Returns:
        Dict: Analysis results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Build query
            query = select(
                Tool.name,
                Tool.type,
                Tool.category,
                func.count(ToolExecution.id).label("execution_count"),
                func.avg(ToolExecution.execution_time).label("avg_execution_time"),
                func.max(ToolExecution.execution_time).label("max_execution_time"),
                func.min(ToolExecution.execution_time).label("min_execution_time")
            ).join(
                ToolExecution,
                Tool.id == ToolExecution.tool_id
            ).where(
                ToolExecution.created_at >= datetime.utcnow() - timedelta(days=days)
            ).group_by(
                Tool.name,
                Tool.type,
                Tool.category
            ).order_by(
                func.count(ToolExecution.id).desc()
            )
            
            # Apply filters
            if tool_type:
                query = query.where(Tool.type == tool_type)
            if category:
                query = query.where(Tool.category == category)
            
            # Execute query
            result = await db_session.execute(query)
            usage_stats = result.fetchall()
            
            # Convert to dictionary
            analysis_results = []
            for stat in usage_stats:
                analysis_results.append({
                    "tool_name": stat.name,
                    "tool_type": stat.type,
                    "category": stat.category,
                    "execution_count": stat.execution_count,
                    "avg_execution_time": float(stat.avg_execution_time or 0),
                    "max_execution_time": float(stat.max_execution_time or 0),
                    "min_execution_time": float(stat.min_execution_time or 0)
                })
            
            logger.info(f"Tool usage analysis completed: {len(analysis_results)} tools analyzed")
            
            return {
                "status": "completed",
                "analysis_time": (datetime.utcnow() - start_time).total_seconds(),
                "days_analyzed": days,
                "tools_analyzed": len(analysis_results),
                "usage_stats": analysis_results
            }
            
    except Exception as e:
        logger.error(f"Error analyzing tool usage: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "analysis_time": (datetime.utcnow() - start_time).total_seconds()
        }