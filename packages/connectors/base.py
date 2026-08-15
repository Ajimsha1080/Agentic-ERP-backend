from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from datetime import datetime

class BaseConnector(ABC):
    """
    Abstract Base Class for all Enterprise Connectors.
    Every integration (SAP, Salesforce, Custom API) MUST implement this interface.
    """

    def __init__(self, tenant_id: str, organization_id: str, credentials: Dict[str, Any]):
        self.tenant_id = tenant_id
        self.organization_id = organization_id
        self.credentials = credentials  # Must be passed securely, never logged

    @abstractmethod
    async def authenticate(self) -> bool:
        """Authenticate with the target system."""
        pass

    @abstractmethod
    async def test_connection(self) -> Dict[str, Any]:
        """Test connection and return health/status data."""
        pass

    @abstractmethod
    async def discover_capabilities(self) -> List[str]:
        """Return a list of supported modules/endpoints (e.g., ['inventory', 'customers'])."""
        pass

    @abstractmethod
    async def get_schema(self, entity_type: str) -> Dict[str, Any]:
        """Fetch the schema/metadata for a given entity type."""
        pass

    @abstractmethod
    async def read(self, entity_type: str, query: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """Read data from the source system."""
        pass

    @abstractmethod
    async def create(self, entity_type: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Create a new record in the source system."""
        pass

    @abstractmethod
    async def update(self, entity_type: str, record_id: str, data: Dict[str, Any]) -> Dict[str, Any]:
        """Update an existing record."""
        pass

    @abstractmethod
    async def delete(self, entity_type: str, record_id: str) -> bool:
        """Delete a record."""
        pass

    @abstractmethod
    async def sync(self, since: Optional[datetime] = None) -> Dict[str, Any]:
        """
        Trigger a batch synchronization.
        If `since` is provided, performs an incremental sync.
        """
        pass

    @abstractmethod
    async def health_check(self) -> bool:
        """Quick ping to verify the connection is still alive."""
        pass

    @abstractmethod
    async def disconnect(self) -> bool:
        """Cleanly close connection and invalidate sessions/tokens."""
        pass
