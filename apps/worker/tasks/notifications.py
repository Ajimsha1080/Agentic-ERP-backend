"""
Notification tasks.

Background tasks for sending notifications and alerts.
"""

from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional
from uuid import UUID
import logging
import asyncio
import smtplib
import requests
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from celery import shared_task
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, and_, func

from packages.database import get_async_db_session
from packages.models import (
    User, WorkflowExecution, AgentExecution, 
    Workflow, Tool, NotificationTemplate, Notification
)
from packages.config import get_settings

logger = logging.getLogger(__name__)
settings = get_settings()


@shared_task(bind=True, name="notifications.send_alerts")
async def send_alerts_task(
    self,
    alert_type: str,
    recipient_ids: List[str],
    alert_data: Dict[str, Any]
) -> Dict[str, Any]:
    """Send alerts to specified recipients asynchronously.
    
    Args:
        alert_type: Type of alert
        recipient_ids: List of user IDs
        alert_data: Alert data and metadata
        
    Returns:
        Dict: Send results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Get recipient details
            from uuid import uuid4
            notification_results = {
                "status": "completed",
                "alert_type": alert_type,
                "recipients": len(recipient_ids),
                "successful": 0,
                "failed": 0,
                "failures": [],
                "notification_time": (datetime.utcnow() - start_time).total_seconds()
            }
            
            for recipient_id in recipient_ids:
                try:
                    # Get user details
                    user_result = await db_session.execute(select(User).where(User.id == UUID(recipient_id)))
                    user = user_result.scalar_one_or_none()
                    
                    if not user:
                        notification_results["failed"] += 1
                        notification_results["failures"].append(f"User {recipient_id} not found")
                        continue
                    
                    # Create notification record
                    notification = Notification(
                        user_id=user.id,
                        type=alert_type,
                        title=alert_data.get("title", f"Alert: {alert_type}"),
                        message=alert_data.get("message", "An alert has been triggered"),
                        data=alert_data,
                        status="pending"
                    )
                    db_session.add(notification)
                    await db_session.commit()
                    await db_session.refresh(notification)
                    
                    # Notification sending logic (mocked for now)
                    
                    # Simulate notification sending
                    channels = user.notification_preferences or {"email": True, "push": True}
                    
                    # Send email notification
                    if channels.get("email", True):
                        await _send_email_notification(
                            user.email,
                            notification.title,
                            notification.message,
                            alert_data
                        )
                    
                    # Send push notification
                    if channels.get("push", True):
                        await _send_push_notification(
                            user.notification_preferences.get("push_token"),
                            notification.title,
                            notification.message
                        )
                    
                    # Update notification status
                    notification.status = "sent"
                    notification.sent_at = datetime.utcnow()
                    await db_session.commit()
                    
                    notification_results["successful"] += 1
                    logger.info(f"Alert sent to {user.email}: {alert_type}")
                    
                except Exception as e:
                    notification_results["failed"] += 1
                    notification_results["failures"].append(f"Failed to send to {recipient_id}: {str(e)}")
                    logger.error(f"Error sending alert to {recipient_id}: {str(e)}")
            
            logger.info(f"Alerts sent: {notification_results['successful']} successful, {notification_results['failed']} failed")
            
            return notification_results
            
    except Exception as e:
        logger.error(f"Error sending alerts: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "notification_time": (datetime.utcnow() - start_time).total_seconds()
        }


async def _send_email_notification(
    email_address: str,
    subject: str,
    message: str,
    data: Dict[str, Any]
) -> bool:
    """Send email notification."""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = settings.EMAIL_FROM
        msg['To'] = email_address
        msg['Subject'] = subject
        
        # Add HTML body
        html_body = f"""
        <html>
        <body>
            <h2>{subject}</h2>
            <p>{message}</p>
            <hr>
            <p>Sent on: {datetime.utcnow().isoformat()}</p>
        </body>
        </html>
        """
        msg.attach(MIMEText(html_body, 'html'))
        
        # Email sending logic (mocked for now)
        # For now, just log the email
        logger.info(f"Email notification sent to {email_address}: {subject}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error sending email to {email_address}: {str(e)}")
        return False


async def _send_push_notification(
    push_token: Optional[str],
    title: str,
    message: str
) -> bool:
    """Send push notification."""
    try:
        if not push_token:
            return False
        
        # Push notification sending logic (mocked for now)
        # For now, just log the push notification
        logger.info(f"Push notification sent to token {push_token}: {title}")
        
        return True
        
    except Exception as e:
        logger.error(f"Error sending push notification: {str(e)}")
        return False


@shared_task(bind=True, name="notifications.send_workflow_notifications")
async def send_workflow_notifications_task(
    self,
    workflow_execution_id: str
) -> Dict[str, Any]:
    """Send workflow execution notifications asynchronously.
    
    Args:
        workflow_execution_id: Workflow execution ID
        
    Returns:
        Dict: Notification results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Get workflow execution details
            from packages.models import WorkflowExecution
            execution_result = await db_session.execute(
                select(WorkflowExecution).where(WorkflowExecution.id == UUID(workflow_execution_id))
            )
            execution = execution_result.scalar_one_or_none()
            
            if not execution:
                raise ValueError(f"Workflow execution {workflow_execution_id} not found")
            
            # Get workflow details
            workflow_result = await db_session.execute(select(Workflow).where(Workflow.id == execution.workflow_id))
            workflow = workflow_result.scalar_one_or_none()
            
            if not workflow:
                raise ValueError(f"Workflow {execution.workflow_id} not found")
            
            # Get user details
            user_result = await db_session.execute(select(User).where(User.id == execution.user_id))
            user = user_result.scalar_one_or_none()
            
            if not user:
                raise ValueError(f"User {execution.user_id} not found")
            
            # Prepare notification data
            notification_data = {
                "workflow_name": workflow.name,
                "execution_id": str(execution.id),
                "status": execution.status,
                "execution_time": execution.execution_time,
                "created_at": execution.created_at.isoformat(),
                "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
                "error_message": execution.error_message
            }
            
            # Determine notification type based on status
            if execution.status == "completed":
                notification_type = "workflow_completed"
                title = f"Workflow '{workflow.name}' completed successfully"
                message = f"Your workflow '{workflow.name}' has completed successfully in {execution.execution_time:.2f} seconds."
            elif execution.status == "failed":
                notification_type = "workflow_failed"
                title = f"Workflow '{workflow.name}' failed"
                message = f"Your workflow '{workflow.name}' has failed. Error: {execution.error_message}"
            else:
                notification_type = "workflow_started"
                title = f"Workflow '{workflow.name}' started"
                message = f"Your workflow '{workflow.name}' has started execution."
            
            # Create notification
            notification = Notification(
                user_id=user.id,
                type=notification_type,
                title=title,
                message=message,
                data=notification_data,
                status="pending"
            )
            db_session.add(notification)
            await db_session.commit()
            await db_session.refresh(notification)
            
            # Send notification
            channels = user.notification_preferences or {"email": True, "push": True}
            
            # Send email notification
            if channels.get("email", True):
                await _send_email_notification(
                    user.email,
                    title,
                    message,
                    notification_data
                )
            
            # Send push notification
            if channels.get("push", True):
                await _send_push_notification(
                    user.notification_preferences.get("push_token"),
                    title,
                    message
                )
            
            # Update notification status
            notification.status = "sent"
            notification.sent_at = datetime.utcnow()
            await db_session.commit()
            
            logger.info(f"Workflow notification sent: {workflow_execution_id}")
            
            return {
                "status": "completed",
                "workflow_execution_id": workflow_execution_id,
                "notification_type": notification_type,
                "recipient": user.email,
                "notification_time": (datetime.utcnow() - start_time).total_seconds()
            }
            
    except Exception as e:
        logger.error(f"Error sending workflow notifications: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "notification_time": (datetime.utcnow() - start_time).total_seconds()
        }


@shared_task(bind=True, name="notifications.send_agent_notifications")
async def send_agent_notifications_task(
    self,
    agent_execution_id: str
) -> Dict[str, Any]:
    """Send agent execution notifications asynchronously.
    
    Args:
        agent_execution_id: Agent execution ID
        
    Returns:
        Dict: Notification results
    """
    start_time = datetime.utcnow()
    
    try:
        # Get database session
        async for db_session in get_async_db_session():
            # Get agent execution details
            from packages.models import AgentExecution
            execution_result = await db_session.execute(
                select(AgentExecution).where(AgentExecution.id == UUID(agent_execution_id))
            )
            execution = execution_result.scalar_one_or_none()
            
            if not execution:
                raise ValueError(f"Agent execution {agent_execution_id} not found")
            
            # Get agent details
            from packages.models import Agent
            agent_result = await db_session.execute(select(Agent).where(Agent.id == execution.agent_id))
            agent = agent_result.scalar_one_or_none()
            
            if not agent:
                raise ValueError(f"Agent {execution.agent_id} not found")
            
            # Get user details
            user_result = await db_session.execute(select(User).where(User.id == execution.user_id))
            user = user_result.scalar_one_or_none()
            
            if not user:
                raise ValueError(f"User {execution.user_id} not found")
            
            # Prepare notification data
            notification_data = {
                "agent_name": agent.name,
                "execution_id": str(execution.id),
                "status": execution.status,
                "execution_time": execution.execution_time,
                "steps_completed": execution.steps_completed,
                "actions_taken": execution.actions_taken,
                "created_at": execution.created_at.isoformat(),
                "completed_at": execution.completed_at.isoformat() if execution.completed_at else None,
                "error_message": execution.error_message
            }
            
            # Determine notification type based on status
            if execution.status == "completed":
                notification_type = "agent_completed"
                title = f"Agent '{agent.name}' completed successfully"
                message = f"Your agent '{agent.name}' has completed successfully in {execution.execution_time:.2f} seconds."
            elif execution.status == "failed":
                notification_type = "agent_failed"
                title = f"Agent '{agent.name}' failed"
                message = f"Your agent '{agent.name}' has failed. Error: {execution.error_message}"
            else:
                notification_type = "agent_started"
                title = f"Agent '{agent.name}' started"
                message = f"Your agent '{agent.name}' has started execution."
            
            # Create notification
            notification = Notification(
                user_id=user.id,
                type=notification_type,
                title=title,
                message=message,
                data=notification_data,
                status="pending"
            )
            db_session.add(notification)
            await db_session.commit()
            await db_session.refresh(notification)
            
            # Send notification
            channels = user.notification_preferences or {"email": True, "push": True}
            
            # Send email notification
            if channels.get("email", True):
                await _send_email_notification(
                    user.email,
                    title,
                    message,
                    notification_data
                )
            
            # Send push notification
            if channels.get("push", True):
                await _send_push_notification(
                    user.notification_preferences.get("push_token"),
                    title,
                    message
                )
            
            # Update notification status
            notification.status = "sent"
            notification.sent_at = datetime.utcnow()
            await db_session.commit()
            
            logger.info(f"Agent notification sent: {agent_execution_id}")
            
            return {
                "status": "completed",
                "agent_execution_id": agent_execution_id,
                "notification_type": notification_type,
                "recipient": user.email,
                "notification_time": (datetime.utcnow() - start_time).total_seconds()
            }
            
    except Exception as e:
        logger.error(f"Error sending agent notifications: {str(e)}", exc_info=True)
        return {
            "status": "failed",
            "error": str(e),
            "notification_time": (datetime.utcnow() - start_time).total_seconds()
        }