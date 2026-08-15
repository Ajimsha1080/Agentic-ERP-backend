import httpx
from typing import Dict, Any, List, Optional
from datetime import datetime
from packages.connectors.base import BaseConnector

class GenericRestConnector(BaseConnector):
    """
    A generic REST API connector that can interface with any standard HTTP JSON API.
    """

    def __init__(self, tenant_id: str, organization_id: str, credentials: Dict[str, Any]):
        super().__init__(tenant_id, organization_id, credentials)
        self.base_url = credentials.get("base_url", "").rstrip("/")
        self.auth_type = credentials.get("auth_type", "bearer")
        self.api_key = credentials.get("api_key", "")
        self.headers = credentials.get("headers", {})

        if self.auth_type == "bearer":
            self.headers["Authorization"] = f"Bearer {self.api_key}"
        elif self.auth_type == "api_key":
            self.headers["x-api-key"] = self.api_key

        self.client = httpx.AsyncClient(headers=self.headers, timeout=30.0)

    async def authenticate(self) -> bool:
        # For API keys/Bearer tokens, validation usually happens on the first request.
        return True

    async def test_connection(self) -> Dict[str, Any]:
        try:
            # Assuming a generic /health or /ping endpoint, or just fetching the root.
            # In a real dynamic setup, this endpoint would be configurable.
            test_endpoint = self.credentials.get("test_endpoint", "/health")
            response = await self.client.get(f"{self.base_url}{test_endpoint}")
            response.raise_for_status()
            return {
                "status": "Healthy",
                "status_code": response.status_code,
                "latency_ms": response.elapsed.total_seconds() * 1000,
                "message": "Connection successful"
            }
        except Exception as e:
            return {
                "status": "Error",
                "message": str(e)
            }

    async def discover_capabilities(self) -> List[str]:
        # Typically requires an OpenAPI spec endpoint, defaulting to configured capabilities.
        return self.credentials.get("capabilities", ["read_only"])

    async def get_schema(self, entity_type: str) -> Dict[str, Any]:
        return {"type": "object", "properties": {}}

    async def read(self, entity_type: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        # Converts entity type (e.g., 'customers') to endpoint
        endpoint = f"/{entity_type.lower()}"
        response = await self.client.get(f"{self.base_url}{endpoint}", params=query)
        response.raise_for_status()
        data = response.json()
        
        # Handle cases where API wraps data in an array or object
        if isinstance(data, list):
            return data
        elif isinstance(data, dict) and "data" in data:
            return data["data"]
        return [data]

    async def create(self, entity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        endpoint = f"/{entity_type.lower()}"
        response = await self.client.post(f"{self.base_url}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

    async def update(self, entity_type: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        endpoint = f"/{entity_type.lower()}/{record_id}"
        response = await self.client.put(f"{self.base_url}{endpoint}", json=data)
        response.raise_for_status()
        return response.json()

    async def delete(self, entity_type: str, record_id: str) -> bool:
        endpoint = f"/{entity_type.lower()}/{record_id}"
        response = await self.client.delete(f"{self.base_url}{endpoint}")
        response.raise_for_status()
        return True

    async def sync(self, since: Optional[datetime] = None) -> Dict[str, Any]:
        # Batch sync logic would iterate over discovered capabilities and dump to DB
        return {"status": "Sync initiated", "records_processed": 0}

    async def health_check(self) -> bool:
        res = await self.test_connection()
        return res.get("status") == "Healthy"

    async def disconnect(self) -> bool:
        await self.client.aclose()
        return True
