"""
Connector tasks.

Background tasks for external service connector operations.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
import requests

from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, and_, func

from packages.database import get_async_db_session
from packages.models import Connector, Connection, ConnectionLog
from packages.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@shared_task(bind=True, name="connector.test_connection")
async def test_connection_task(
    self,
    connection_id: str,
    test_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Test a connection asynchronously.
    
    Args:
        connection_id: Connection ID
        test_config: Optional test configuration
        
    Returns:
        Dict: Test results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Get connection details
            connection_result = await db_session.execute(
                select(Connection).where(Connection.id == UUID(connection_id))
            )
            connection = connection_result.scalar_one_or_none()
            
            if not connection:
                raise ValueError(f"Connection {connection_id} not found")
            
            # Get connector details
            connector_result = await db_session.execute(
                select(Connector).where(Connector.id == connection.connector_id)
            )
            connector = connector_result.scalar_one_or_none()
            
            if not connector:
                raise ValueError(f"Connector {connection.connector_id} not found")
            
            # Prepare test configuration
            config = test_config or connection.config or {}
            
            # Connection test logic (mocked for now)
            
            # Simulate connection test
            import random
            success = random.random() > 0.1  # 90% chance of success
            
            test_results = {
                "status": "success" if success else "failed",
                "connector_type": connector.service_type,
                "connection_name": connection.name,
                "test_time": (datetime.utcnow() - start_time).total_seconds(),
                "response_time": random.uniform(0.5, 3.0),
                "details": {}
            }
            
            # Add connector-specific test results
            if connector.service_type == "api":
                test_results["details"] = {
                    "api_calls": 3,
                    "status_codes": [200, 200, 200] if success else [200, 404, 500],
                    "endpoints_tested": ["/health", "/status", "/info"]
                }
            elif connector.service_type == "database":
                test_results["details"] = {
                    "connection_successful": success,
                    "query_executed": "SELECT 1",
                    "response_time_ms": random.uniform(10, 100),
                    "database_type": "postgresql"
                }
            elif connector.service_type == "email":
                test_results["details"] = {
                    "server_reachable": success,
                    "protocol": "smtp",
                    "port": 587,
                    "ssl_enabled": True
                }
            
            # Update connection status
            if success:
                connection.status = "active"
                connection.last_connected_at = datetime.utcnow()
            else:
                connection.status = "error"
            
            # Log the test
            log = ConnectionLog(
                connection_id=connection.id,
                action="test",
                status=test_results["status"],
                duration=test_results["test_time"],
                response_data=test_results["details"],
                metadata={"test_config": test_config}
            )
            db_session.add(log)
            
            await db_session.commit()
            
            logger.info(f"Connection test completed: {connection_id}")
            
            return test_results
            
    except Exception as e:
        logger.error(f"Error testing connection {connection_id}: {str(e)}", exc_info=True)
        
        # Update connection status on error
        async for db_session in get_async_db_session():
            connection_result = await db_session.execute(
                select(Connection).where(Connection.id == UUID(connection_id))
            )
            connection = connection_result.scalar_one_or_none()
            
            if connection:
                connection.status = "error"
                await db_session.commit()
        
        return {
            "status": "failed",
            "error": str(e),
            "test_time": (datetime.utcnow() - start_time).total_seconds()
        }


@shared_task(bind=True, name="connector.sync_data")
async def sync_data_task(
    self,
    connection_id: str,
    sync_config: Optional[Dict[str, Any]] = None
) -> Dict[str, Any]:
    """Sync data through a connection asynchronously.
    
    Args:
        connection_id: Connection ID
        sync_config: Optional sync configuration
        
    Returns:
        Dict: Sync results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Get connection details
            connection_result = await db_session.execute(
                select(Connection).where(Connection.id == UUID(connection_id))
            )
            connection = connection_result.scalar_one_or_none()
            
            if not connection:
                raise ValueError(f"Connection {connection_id} not found")
            
            # Get connector details
            connector_result = await db_session.execute(
                select(Connector).where(Connector.id == connection.connector_id)
            )
            connector = connector_result.scalar_one_or_none()
            
            if not connector:
                raise ValueError(f"Connector {connection.connector_id} not found")
            
            # Prepare sync configuration
            config = sync_config or connection.config or {}
            
            # Data sync logic (mocked for now)
            
            # Simulate data sync
            import random
            success = random.random() > 0.05  # 95% chance of success
            
            sync_results = {
                "status": "success" if success else "failed",
                "connection_name": connection.name,
                "sync_time": (datetime.utcnow() - start_time).total_seconds(),
                "records_processed": random.randint(100, 1000),
                "records_added": random.randint(50, 500),
                "records_updated": random.randint(10, 100),
                "records_deleted": random.randint(0, 50),
                "errors": [],
                "warnings": []
            }
            
            # Add random errors if failed
            if not success:
                sync_results["errors"] = ["Data sync failed due to timeout"]
                sync_results["records_processed"] = 0
            
            # Update connection last sync time
            if success:
                connection.last_connected_at = datetime.utcnow()
            
            # Log the sync
            log = ConnectionLog(
                connection_id=connection.id,
                action="sync",
                status=sync_results["status"],
                duration=sync_results["sync_time"],
                request_data=config,
                response_data=sync_results,
                metadata={"sync_config": sync_config}
            )
            db_session.add(log)
            
            # Update connector usage stats
            connector.usage_count += 1
            connector.last_used_at = datetime.utcnow()
            
            await db_session.commit()
            
            logger.info(f"Data sync completed: {connection_id}")
            
            return sync_results
            
    except Exception as e:
        logger.error(f"Error syncing data {connection_id}: {str(e)}", exc_info=True)
        
        # Log the error
        async for db_session in get_async_db_session():
            log = ConnectionLog(
                connection_id=UUID(connection_id),
                action="sync",
                status="failed",
                duration=(datetime.utcnow() - start_time).total_seconds(),
                error_message=str(e),
                metadata={"sync_config": sync_config}
            )
            db_session.add(log)
            await db_session.commit()
        
        return {
            "status": "failed",
            "error": str(e),
            "sync_time": (datetime.utcnow() - start_time).total_seconds()
        }


@shared_task(bind=True, name="connector.analyze_connection_usage")
async def analyze_connection_usage_task(
    self,
    days: int = 30,
    connector_type: Optional[str] = None,
    category: Optional[str] = None
) -> Dict[str, Any]:
    """Analyze connector usage patterns asynchronously.
    
    Args:
        days: Number of days to analyze
        connector_type: Optional connector type filter
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
                Connector.name,
                Connector.service_type,
                Connector.category,
                func.count(Connection.id).label("connection_count"),
                func.count(ConnectionLog.id).label("activity_count"),
                func.max(Connection.last_connected_at).label("last_activity")
            ).join(
                Connection,
                Connector.id == Connection.connector_id
            ).outerjoin(
                ConnectionLog,
                Connection.id == ConnectionLog.connection_id
            ).where(
                Connection.created_at >= datetime.utcnow() - timedelta(days=days)
            ).group_by(
                Connector.name,
                Connector.service_type,
                Connector.category
            ).order_by(
                func.count(Connection.id).desc()
            )
            
            # Apply filters
            if connector_type:
                query = query.where(Connector.service_type == connector_type)
            if category:
                query = query.where(Connector.category == category)
            
            # Execute query
            result = await db_session.execute(query)
            usage_stats = result.fetchall()
            
            # Convert to dictionary
            analysis_results = []
            for stat in usage_stats:
                analysis_results.append({
                    "connector_name": stat.name,
                    "service_type": stat.service_type,
                    "category": stat.category,
                    "connection_count": stat.connection_count,
                    "activity_count": stat.activity_count,
                    "last_activity": stat.last_activity.isoformat() if stat.last_activity else None
                })
            
            logger.info(f"Connection usage analysis completed: {len(analysis_results)} connectors analyzed")
            
            return {
                "status": "completed",
                "analysis_time": (datetime.utcnow() - start_time).total_seconds(),
                "days_analyzed": days,
                "connectors_analyzed": len(analysis_results),
                "usage_stats": analysis_results
            }
            
    except Exception as e:
        logger.error(f"Error analyzing connection usage: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "analysis_time": (datetime.utcnow() - start_time).total_seconds()
        }