import logging
from typing import Any, Dict, Optional

from modelscope.hub.mcp_api import MCPApi
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from app.exceptions import (
    AuthenticationError,
    MCPAPIException,
    NetworkError,
    ServerNotFoundError,
)

logger = logging.getLogger(__name__)


class MCPService:
    """Service class for ModelScope MCP operations with error handling and retry logic."""

    def __init__(self, token: Optional[str] = None):
        """
        Initialize MCP service.

        Args:
            token: Optional ModelScope API token.
        """
        self.token = token
        self._api: Optional[MCPApi] = None

    @property
    def api(self) -> MCPApi:
        """Lazy initialization of MCPApi instance."""
        if self._api is None:
            self._api = MCPApi()
            if self.token:
                try:
                    self._api.login(self.token)
                    logger.info("Successfully authenticated with ModelScope")
                except Exception as e:
                    logger.error(f"Authentication failed: {str(e)}")
                    raise AuthenticationError(
                        "Failed to authenticate with ModelScope", detail=str(e)
                    )
        return self._api

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(NetworkError),
        reraise=True,
    )
    def list_mcp_servers(
        self,
        filter_criteria: Optional[Dict[str, Any]] = None,
        total_count: int = 20,
        search: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        List MCP servers with optional filtering and search.

        Args:
            filter_criteria: Filter by category, tag, or is_hosted
            total_count: Number of results (1-100)
            search: Search keyword

        Returns:
            Dictionary with total_count and servers list

        Raises:
            AuthenticationError: If authentication fails
            NetworkError: If network request fails
            MCPAPIException: For other API errors
        """
        try:
            logger.info(
                f"Listing MCP servers: filter={filter_criteria}, "
                f"count={total_count}, search={search}"
            )

            kwargs: Dict[str, Any] = {"total_count": total_count}
            if filter_criteria:
                kwargs["filter"] = filter_criteria
            if search:
                kwargs["search"] = search

            result = self.api.list_mcp_servers(**kwargs)
            logger.info(f"Found {result.get('total_count', 0)} MCP servers")
            return result

        except Exception as e:
            logger.error(f"Failed to list MCP servers: {str(e)}")
            if "network" in str(e).lower() or "connection" in str(e).lower():
                raise NetworkError("Network error while listing servers", detail=str(e))
            raise MCPAPIException("Failed to list MCP servers", detail=str(e))

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(NetworkError),
        reraise=True,
    )
    def list_operational_mcp_servers(self) -> Dict[str, Any]:
        """
        List operational (activated) MCP servers.

        Returns:
            Dictionary with total_count and servers list with endpoints

        Raises:
            AuthenticationError: If not authenticated or token invalid
            NetworkError: If network request fails
            MCPAPIException: For other API errors
        """
        if not self.token:
            raise AuthenticationError(
                "Authentication required",
                detail="Token must be provided to list operational servers",
            )

        try:
            logger.info("Listing operational MCP servers")
            result = self.api.list_operational_mcp_servers()
            logger.info(f"Found {result.get('total_count', 0)} operational servers")
            return result

        except Exception as e:
            logger.error(f"Failed to list operational servers: {str(e)}")
            if "auth" in str(e).lower() or "permission" in str(e).lower():
                raise AuthenticationError("Authentication failed", detail=str(e))
            if "network" in str(e).lower() or "connection" in str(e).lower():
                raise NetworkError(
                    "Network error while listing operational servers", detail=str(e)
                )
            raise MCPAPIException("Failed to list operational servers", detail=str(e))

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=2, max=10),
        retry=retry_if_exception_type(NetworkError),
        reraise=True,
    )
    def get_mcp_server(self, server_id: str) -> Dict[str, Any]:
        """
        Get detailed information about a specific MCP server.

        Args:
            server_id: Server ID in format @group/name

        Returns:
            Dictionary with server details and endpoints

        Raises:
            ServerNotFoundError: If server doesn't exist
            NetworkError: If network request fails
            MCPAPIException: For other API errors
        """
        try:
            logger.info(f"Getting MCP server details: {server_id}")
            result = self.api.get_mcp_server(server_id=server_id)
            logger.info(f"Successfully retrieved server: {server_id}")
            return result

        except Exception as e:
            error_msg = str(e).lower()
            logger.error(f"Failed to get MCP server {server_id}: {str(e)}")

            if "not found" in error_msg or "does not exist" in error_msg:
                raise ServerNotFoundError(
                    f"MCP server '{server_id}' not found", detail=str(e)
                )
            if "network" in error_msg or "connection" in error_msg:
                raise NetworkError(
                    f"Network error while getting server {server_id}", detail=str(e)
                )
            raise MCPAPIException(
                f"Failed to get MCP server '{server_id}'", detail=str(e)
            )
