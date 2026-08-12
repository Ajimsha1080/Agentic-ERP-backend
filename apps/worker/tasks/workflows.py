"""
Workflow tasks.

Background tasks for AI workflow operations.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
import asyncio
import random

from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, func

from packages.database import get_async_db_session
from packages.models import Workflow, WorkflowExecution, WorkflowTemplate, WorkflowExecutionLog, WorkflowStatus
from packages.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@shared_task(bind=True, name="workflow.execute_workflow")
async def execute_workflow_task(
    self,
    workflow_id: str,
    user_id: str,
    agent_id: Optional[str] = None,
    trigger_type: Optional[str] = None,
    input_data: Optional[Dict[str, Any]] = None,
    config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Execute a workflow asynchronously.
    
    Args:
        workflow_id: Workflow ID
        user_id: User ID
        agent_id: Optional agent ID
        trigger_type: Workflow trigger type
        input_data: Input data for the workflow
        config: Optional configuration override
        
    Returns:
        Dict: Execution results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Get workflow details
            workflow_result = await db_session.execute(select(Workflow).where(Workflow.id == UUID(workflow_id)))
            workflow = workflow_result.scalar_one_or_none()
            
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found")
            
            # Check if workflow is active
            if workflow.status != WorkflowStatus.ACTIVE:
                raise ValueError(f"Workflow {workflow_id} is not active")
            
            # Get user details
            from packages.models import User
            user_result = await db_session.execute(select(User).where(User.id == UUID(user_id)))
            user = user_result.scalar_one_or_none()
            
            if not user:
                raise ValueError(f"User {user_id} not found")
            
            # Create execution record
            execution = WorkflowExecution(
                workflow_id=UUID(workflow_id),
                user_id=UUID(user_id),
                agent_id=UUID(agent_id) if agent_id else None,
                trigger_type=trigger_type,
                input_data=input_data,
                config=config,
                status="running",
                started_at=start_time
            )
            db_session.add(execution)
            await db_session.commit()
            await db_session.refresh(execution)
            
            # Add initial log
            initial_log = WorkflowExecutionLog(
                workflow_execution_id=execution.id,
                level="INFO",
                message=f"Workflow execution started for workflow {workflow.name}",
                step="start",
                metadata={
                    "workflow_name": workflow.name,
                    "trigger_type": trigger_type
                }
            )
            db_session.add(initial_log)
            
            # Workflow execution logic (mocked for now)
            
            # Simulate workflow execution
            steps = workflow.steps or [
                {"name": "data_retrieval", "type": "tool", "input": {"source": "database"}},
                {"name": "data_processing", "type": "transformation", "input": {"operation": "clean"}},
                {"name": "analysis", "type": "ai", "input": {"model": "analysis"}},
                {"name": "reporting", "type": "generation", "input": {"format": "pdf"}},
                {"name": "notification", "type": "communication", "input": {"recipients": ["user"]}}
            ]
            
            total_steps = len(steps)
            execution.current_step = 0
            execution.total_steps = total_steps
            
            for i, step in enumerate(steps):
                execution.current_step = i + 1
                await db_session.commit()
                
                # Add step log
                step_log = WorkflowExecutionLog(
                    workflow_execution_id=execution.id,
                    level="INFO",
                    message=f"Executing step: {step['name']}",
                    step=step["name"],
                    metadata={"step_index": i + 1, "step_type": step["type"]}
                )
                db_session.add(step_log)
                
                # Simulate step execution
                await asyncio.sleep(1)
                
                # Simulate occasional step failures
                if random.random() < 0.05:  # 5% chance of step failure
                    execution.status = "failed"
                    execution.current_step = i + 1
                    execution.error_message = f"Step '{step['name']}' failed"
                    
                    error_log = WorkflowExecutionLog(
                        workflow_execution_id=execution.id,
                        level="ERROR",
                        message=f"Step failed: {step['name']}",
                        step=step["name"],
                        metadata={"error": execution.error_message}
                    )
                    db_session.add(error_log)
                    await db_session.commit()
                    raise ValueError(execution.error_message)
                
                # Add step completion log
                completion_log = WorkflowExecutionLog(
                    workflow_execution_id=execution.id,
                    level="INFO",
                    message=f"Step completed: {step['name']}",
                    step=step["name"],
                    metadata={"execution_time": 1.0}
                )
                db_session.add(completion_log)
            
            # Complete execution
            execution.status = "completed"
            execution.completed_at = datetime.utcnow()
            execution.execution_time = (datetime.utcnow() - start_time).total_seconds()
            execution.output_data = {
                "result": "Workflow execution completed successfully",
                "steps_completed": total_steps,
                "execution_time": execution.execution_time,
                "output_data": {
                    "summary": "All steps completed successfully",
                    "results": [f"step_{i+1}_result" for i in range(total_steps)]
                }
            }
            
            # Add completion log
            completion_log = WorkflowExecutionLog(
                workflow_execution_id=execution.id,
                level="INFO",
                message="Workflow execution completed successfully",
                step="completion",
                metadata={
                    "total_steps": total_steps,
                    "execution_time": execution.execution_time
                }
            )
            db_session.add(completion_log)
            
            # Update workflow usage stats
            workflow.usage_count += 1
            workflow.last_used_at = datetime.utcnow()
            
            await db_session.commit()
            
            logger.info(f"Workflow execution completed: {workflow_id}")
            
            return {
                "execution_id": str(execution.id),
                "status": "completed",
                "output": execution.output_data,
                "execution_time": execution.execution_time,
                "workflow_name": workflow.name
            }
            
    except Exception as e:
        logger.error(f"Error executing workflow {workflow_id}: {str(e)}", exc_info=True)
        
        # Update execution record with error
        async for db_session in get_async_db_session():
            execution_result = await db_session.execute(
                select(WorkflowExecution).where(WorkflowExecution.id == execution.id)
            )
            execution = execution_result.scalar_one_or_none()
            
            if execution:
                execution.status = "failed"
                execution.completed_at = datetime.utcnow()
                execution.execution_time = (datetime.utcnow() - start_time).total_seconds()
                execution.error_message = str(e)
                
                # Add error log
                error_log = WorkflowExecutionLog(
                    workflow_execution_id=execution.id,
                    level="ERROR",
                    message=f"Workflow execution failed: {str(e)}",
                    step="error",
                    metadata={"error": str(e)}
                )
                db_session.add(error_log)
                await db_session.commit()
        
        return {
            "execution_id": str(execution.id) if execution else "unknown",
            "status": "failed",
            "error": str(e),
            "execution_time": (datetime.utcnow() - start_time).total_seconds()
        }


@shared_task(bind=True, name="workflow.schedule_workflow")
async def schedule_workflow_task(
    self,
    workflow_id: str,
    schedule_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Schedule a workflow asynchronously.
    
    Args:
        workflow_id: Workflow ID
        schedule_config: Schedule configuration
        
    Returns:
        Dict: Schedule results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Get workflow details
            workflow_result = await db_session.execute(select(Workflow).where(Workflow.id == UUID(workflow_id)))
            workflow = workflow_result.scalar_one_or_none()
            
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found")
            
            # Workflow scheduling logic (mocked for now)
            
            # Simulate scheduling
            schedule_results = {
                "status": "completed",
                "workflow_name": workflow.name,
                "schedule_type": schedule_config.get("type", "cron"),
                "schedule_expression": schedule_config.get("expression", "0 0 * * *"),
                "next_run": datetime.utcnow().isoformat(),
                "timezone": schedule_config.get("timezone", "UTC"),
                "schedule_time": (datetime.utcnow() - start_time).total_seconds()
            }
            
            # Update workflow schedule
            workflow.schedule = schedule_config
            await db_session.commit()
            
            logger.info(f"Workflow scheduled: {workflow_id}")
            
            return schedule_results
            
    except Exception as e:
        logger.error(f"Error scheduling workflow {workflow_id}: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "schedule_time": (datetime.utcnow() - start_time).total_seconds()
        }


@shared_task(bind=True, name="workflow.create_from_template")
async def create_workflow_from_template_task(
    self,
    template_id: str,
    workflow_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Create workflow from template asynchronously.
    
    Args:
        template_id: Template ID
        workflow_config: Workflow configuration
        
    Returns:
        Dict: Creation results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Get template details
            template_result = await db_session.execute(select(WorkflowTemplate).where(WorkflowTemplate.id == UUID(template_id)))
            template = template_result.scalar_one_or_none()
            
            if not template:
                raise ValueError(f"Template {template_id} not found")
            
            # Create workflow from template
            workflow = Workflow(
                name=workflow_config.get("name", f"Workflow from {template.name}"),
                description=workflow_config.get("description", template.description),
                agent_id=workflow_config.get("agent_id"),
                category=workflow_config.get("category", template.category),
                version="1.0.0",
                status=WorkflowStatus.ACTIVE,
                config_schema=workflow_config.get("config_schema", template.config_schema),
                input_schema=workflow_config.get("input_schema", template.input_schema),
                output_schema=workflow_config.get("output_schema", template.output_schema),
                steps=workflow_config.get("steps", template.steps),
                triggers=workflow_config.get("triggers", template.triggers),
                schedule=workflow_config.get("schedule"),
                author=workflow_config.get("author"),
                tags=workflow_config.get("tags", template.tags),
                is_enabled=workflow_config.get("is_enabled", True),
                is_public=workflow_config.get("is_public", False)
            )
            db_session.add(workflow)
            await db_session.commit()
            await db_session.refresh(workflow)
            
            # Update template usage stats
            template.usage_count += 1
            await db_session.commit()
            
            logger.info(f"Workflow created from template: {template_id} -> {workflow.id}")
            
            return {
                "status": "completed",
                "workflow_id": str(workflow.id),
                "workflow_name": workflow.name,
                "template_id": str(template_id),
                "template_name": template.name,
                "creation_time": (datetime.utcnow() - start_time).total_seconds()
            }
            
    except Exception as e:
        logger.error(f"Error creating workflow from template {template_id}: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "creation_time": (datetime.utcnow() - start_time).total_seconds()
        }


@shared_task(bind=True, name="workflow.optimize_workflow")
async def optimize_workflow_task(
    self,
    workflow_id: str,
    optimization_config: Dict[str, Any]
) -> Dict[str, Any]:
    """Optimize workflow asynchronously.
    
    Args:
        workflow_id: Workflow ID
        optimization_config: Optimization configuration
        
    Returns:
        Dict: Optimization results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Get workflow details
            workflow_result = await db_session.execute(select(Workflow).where(Workflow.id == UUID(workflow_id)))
            workflow = workflow_result.scalar_one_or_none()
            
            if not workflow:
                raise ValueError(f"Workflow {workflow_id} not found")
            
            # Workflow optimization logic (mocked for now)
            
            # Simulate optimization
            optimization_results = {
                "status": "completed",
                "workflow_name": workflow.name,
                "optimization_time": (datetime.utcnow() - start_time).total_seconds(),
                "improvements": [
                    {"metric": "execution_time", "improvement": 0.15, "value": "15% faster"},
                    {"metric": "resource_usage", "improvement": 0.25, "value": "25% less memory"},
                    {"metric": "success_rate", "improvement": 0.05, "value": "5% more reliable"}
                ],
                "applied_changes": [
                    "Parallelized data retrieval steps",
                    "Optimized data processing pipeline",
                    "Added error handling for critical steps"
                ],
                "new_config": {
                    "parallel_execution": True,
                    "timeout_per_step": 60,
                    "retry_count": 3,
                    "cache_enabled": True
                }
            }
            
            # Update workflow configuration
            if "config" in optimization_config:
                workflow.config_schema = optimization_config["config"]
            
            workflow.updated_at = datetime.utcnow()
            await db_session.commit()
            
            logger.info(f"Workflow optimized: {workflow_id}")
            
            return optimization_results
            
    except Exception as e:
        logger.error(f"Error optimizing workflow {workflow_id}: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "optimization_time": (datetime.utcnow() - start_time).total_seconds()
        }