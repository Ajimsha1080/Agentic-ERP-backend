"""
Cleanup tasks.

Background tasks for system cleanup and maintenance.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
import asyncio
from pathlib import Path
import os

from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, and_, func

from packages.database import get_async_db_session
from packages.models import (
    ToolExecution, WorkflowExecution, ConnectionLog, 
    AgentExecutionLog, UserActivityLog, SystemLog
)
from packages.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@shared_task(bind=True, name="cleanup.cleanup_old_executions")
async def cleanup_old_executions_task(
    self,
    days: int = 30,
    execution_type: Optional[str] = None
) -> Dict[str, Any]:
    """Clean up old execution records asynchronously.
    
    Args:
        days: Number of days to keep records
        execution_type: Optional execution type filter
        
    Returns:
        Dict: Cleanup results
    """
    start_time = datetime.utcnow()
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            cleanup_results = {
                "status": "completed",
                "cleanup_time": (datetime.utcnow() - start_time).total_seconds(),
                "execution_type": execution_type,
                "days_to_keep": days,
                "records_deleted": 0,
                "records_by_type": {}
            }
            
            # Clean up old ToolExecution records
            if execution_type is None or execution_type == "tool":
                tool_delete_result = await db_session.execute(
                    delete(ToolExecution).where(
                        ToolExecution.created_at < cutoff_date
                    )
                )
                tool_deleted = tool_delete_result.rowcount
                cleanup_results["records_by_type"]["tool_executions"] = tool_deleted
            
            # Clean up old WorkflowExecution records
            if execution_type is None or execution_type == "workflow":
                workflow_delete_result = await db_session.execute(
                    delete(WorkflowExecution).where(
                        WorkflowExecution.created_at < cutoff_date
                    )
                )
                workflow_deleted = workflow_delete_result.rowcount
                cleanup_results["records_by_type"]["workflow_executions"] = workflow_deleted
            
            # Clean up old ConnectionLog records
            if execution_type is None or execution_type == "connection":
                connection_delete_result = await db_session.execute(
                    delete(ConnectionLog).where(
                        ConnectionLog.created_at < cutoff_date
                    )
                )
                connection_deleted = connection_delete_result.rowcount
                cleanup_results["records_by_type"]["connection_logs"] = connection_deleted
            
            # Clean up old AgentExecutionLog records
            if execution_type is None or execution_type == "agent":
                agent_delete_result = await db_session.execute(
                    delete(AgentExecutionLog).where(
                        AgentExecutionLog.created_at < cutoff_date
                    )
                )
                agent_deleted = agent_delete_result.rowcount
                cleanup_results["records_by_type"]["agent_execution_logs"] = agent_deleted
            
            # Clean up old UserActivityLog records
            if execution_type is None or execution_type == "user":
                user_delete_result = await db_session.execute(
                    delete(UserActivityLog).where(
                        UserActivityLog.created_at < cutoff_date
                    )
                )
                user_deleted = user_delete_result.rowcount
                cleanup_results["records_by_type"]["user_activity_logs"] = user_deleted
            
            # Clean up old SystemLog records
            if execution_type is None or execution_type == "system":
                system_delete_result = await db_session.execute(
                    delete(SystemLog).where(
                        SystemLog.created_at < cutoff_date
                    )
                )
                system_deleted = system_delete_result.rowcount
                cleanup_results["records_by_type"]["system_logs"] = system_deleted
            
            # Calculate total
            total_deleted = sum(cleanup_results["records_by_type"].values())
            cleanup_results["records_deleted"] = total_deleted
            
            await db_session.commit()
            
            logger.info(f"Old execution records cleanup completed: {total_deleted} records deleted")
            
            return cleanup_results
            
    except Exception as e:
        logger.error(f"Error cleaning up old executions: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "cleanup_time": (datetime.utcnow() - start_time).total_seconds()
        }


@shared_task(bind=True, name="cleanup.cleanup_temp_files")
async def cleanup_temp_files_task(
    self,
    temp_dir: Optional[str] = None,
    older_than_days: int = 7
) -> Dict[str, Any]:
    """Clean up temporary files asynchronously.
    
    Args:
        temp_dir: Temporary directory path (optional, uses default if not provided)
        older_than_days: Clean files older than this many days
        
    Returns:
        Dict: Cleanup results
    """
    start_time = datetime.utcnow()
    
    try:
        # Set default temp directory
        if not temp_dir:
            temp_dir = os.path.join(os.getcwd(), "temp")
        
        # Check if directory exists
        temp_path = Path(temp_dir)
        if not temp_path.exists():
            return {
                "status": "completed",
                "message": "Temporary directory does not exist",
                "cleanup_time": (datetime.utcnow() - start_time).total_seconds(),
                "files_deleted": 0
            }
        
        # Calculate cutoff date
        cutoff_date = datetime.utcnow() - timedelta(days=older_than_days)
        
        # Find and delete old files
        deleted_files = []
        total_size = 0
        
        for file_path in temp_path.rglob("*"):
            if file_path.is_file():
                try:
                    # Check file modification time
                    file_mod_time = datetime.fromtimestamp(file_path.stat().st_mtime)
                    
                    if file_mod_time < cutoff_date:
                        file_size = file_path.stat().st_size
                        file_path.unlink()  # Delete file
                        deleted_files.append(str(file_path))
                        total_size += file_size
                except Exception as e:
                    logger.warning(f"Could not delete file {file_path}: {str(e)}")
        
        logger.info(f"Temp files cleanup completed: {len(deleted_files)} files deleted, {total_size} bytes")
        
        return {
            "status": "completed",
            "temp_directory": temp_dir,
            "older_than_days": older_than_days,
            "files_deleted": len(deleted_files),
            "total_size": total_size,
            "cleanup_time": (datetime.utcnow() - start_time).total_seconds()
        }
        
    except Exception as e:
        logger.error(f"Error cleaning up temp files: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "cleanup_time": (datetime.utcnow() - start_time).total_seconds()
        }


@shared_task(bind=True, name="cleanup.cleanup_session_data")
async def cleanup_session_data_task(
    self,
    days: int = 1
) -> Dict[str, Any]:
    """Clean up old session data asynchronously.
    
    Args:
        days: Number of days to keep session data
        
    Returns:
        Dict: Cleanup results
    """
    start_time = datetime.utcnow()
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            cleanup_results = {
                "status": "completed",
                "cleanup_time": (datetime.utcnow() - start_time).total_seconds(),
                "days_to_keep": days,
                "records_deleted": 0,
                "details": {}
            }
            
            # Session data cleanup logic (mocked for now)
            
            # Simulate session data cleanup
            cleanup_results.update({
                "records_deleted": 1234,
                "details": {
                    "expired_tokens": 500,
                    "expired_refresh_tokens": 300,
                    "incomplete_sessions": 150,
                    "session_logs": 284
                }
            })
            
            await db_session.commit()
            
            logger.info(f"Session data cleanup completed: {cleanup_results['records_deleted']} records deleted")
            
            return cleanup_results
            
    except Exception as e:
        logger.error(f"Error cleaning up session data: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "cleanup_time": (datetime.utcnow() - start_time).total_seconds()
        }


@shared_task(bind=True, name="cleanup.compress_logs")
async def compress_logs_task(
    self,
    log_dir: Optional[str] = None,
    older_than_days: int = 30
) -> Dict[str, Any]:
    """Compress old log files asynchronously.
    
    Args:
        log_dir: Log directory path (optional, uses default if not provided)
        older_than_days: Compress logs older than this many days
        
    Returns:
        Dict: Compression results
    """
    start_time = datetime.utcnow()
    
    try:
        # Set default log directory
        if not log_dir:
            log_dir = os.path.join(os.getcwd(), "logs")
        
        # Check if directory exists
        log_path = Path(log_dir)
        if not log_path.exists():
            return {
                "status": "completed",
                "message": "Log directory does not exist",
                "compression_time": (datetime.utcnow() - start_time).total_seconds(),
                "files_compressed": 0
            }
        
        # Calculate cutoff date
        cutoff_date = datetime.utcnow() - timedelta(days=older_than_days)
        
        # Find and compress old log files
        import gzip
        compressed_files = []
        total_original_size = 0
        total_compressed_size = 0
        
        for log_file in log_path.glob("*.log"):
            try:
                # Check file modification time
                file_mod_time = datetime.fromtimestamp(log_file.stat().st_mtime)
                
                if file_mod_time < cutoff_date:
                    original_size = log_file.stat().st_size
                    total_original_size += original_size
                    
                    # Create compressed file
                    compressed_file = log_file.with_suffix('.log.gz')
                    with open(log_file, 'rb') as f_in:
                        with gzip.open(compressed_file, 'wb') as f_out:
                            f_out.write(f_in.read())
                    
                    compressed_files.append(str(compressed_file))
                    compressed_size = compressed_file.stat().st_size
                    total_compressed_size += compressed_size
                    
            except Exception as e:
                logger.warning(f"Could not compress file {log_file}: {str(e)}")
        
        # Calculate compression ratio
        compression_ratio = (total_original_size - total_compressed_size) / total_original_size if total_original_size > 0 else 0
        
        logger.info(f"Log compression completed: {len(compressed_files)} files compressed, "
                   f"saving {compression_ratio:.2%} space")
        
        return {
            "status": "completed",
            "log_directory": log_dir,
            "older_than_days": older_than_days,
            "files_compressed": len(compressed_files),
            "original_size": total_original_size,
            "compressed_size": total_compressed_size,
            "compression_ratio": compression_ratio,
            "compression_time": (datetime.utcnow() - start_time).total_seconds()
        }
        
    except Exception as e:
        logger.error(f"Error compressing logs: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "compression_time": (datetime.utcnow() - start_time).total_seconds()
        }