from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from uuid import UUID

from packages.connectors.generic_rest import GenericRestConnector

router = APIRouter(prefix="/connectors", tags=["Connectors"])

class ConnectorCredentials(BaseModel):
    integration_type: str  # e.g., 'sap', 'salesforce', 'rest'
    organization_id: str
    credentials: Dict[str, Any]

class ConnectionTestResponse(BaseModel):
    status: str
    message: str
    latency_ms: Optional[float] = None
    capabilities: Optional[List[str]] = None

@router.get("/available")
async def get_available_connectors():
    """List all integrations supported by the platform."""
    return [
        {"id": "sap", "name": "SAP S/4HANA", "status": "Available", "type": "erp"},
        {"id": "salesforce", "name": "Salesforce", "status": "Available", "type": "crm"},
        {"id": "shopify", "name": "Shopify", "status": "Available", "type": "ecommerce"},
        {"id": "zoho", "name": "Zoho Books", "status": "Coming Soon", "type": "finance"},
        {"id": "custom", "name": "Custom REST API", "status": "Available", "type": "generic"}
    ]

@router.post("/test", response_model=ConnectionTestResponse)
async def test_connection(data: ConnectorCredentials):
    """
    Test the connection to an ERP securely.
    Instantiates the connector, runs the test, and immediately discards the credentials.
    """
    # Factory logic to pick the right connector class
    if data.integration_type in ["rest", "custom", "shopify"]:
        connector = GenericRestConnector(
            tenant_id="test_tenant",
            organization_id=data.organization_id,
            credentials=data.credentials
        )
    else:
        # Fallback to Generic for MVP simulation of SAP/Oracle if specific classes aren't loaded
        connector = GenericRestConnector(
            tenant_id="test_tenant", 
            organization_id=data.organization_id, 
            credentials=data.credentials
        )

    try:
        # 1. Authenticate
        auth_success = await connector.authenticate()
        if not auth_success:
            raise HTTPException(status_code=401, detail="Authentication failed")

        # 2. Test Connection
        test_result = await connector.test_connection()
        
        # 3. Discover Capabilities
        capabilities = await connector.discover_capabilities()

        return ConnectionTestResponse(
            status=test_result.get("status", "Healthy"),
            message=test_result.get("message", "Connection successful"),
            latency_ms=test_result.get("latency_ms"),
            capabilities=capabilities
        )
    except Exception as e:
        return ConnectionTestResponse(
            status="Error",
            message=str(e)
        )