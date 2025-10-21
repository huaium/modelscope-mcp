from typing import Any, Dict, List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class MCPServerInfo(BaseModel):
    """Basic MCP server information."""

    name: str = Field(..., description="Server name")
    id: str = Field(..., description="Server ID in format @group/name")
    description: str = Field(..., description="Server description")


class MCPServerEndpoint(BaseModel):
    """MCP server endpoint configuration."""

    type: Literal["sse", "streamable_http"] = Field(..., description="Endpoint type")
    url: str = Field(..., description="Endpoint URL")


class MCPServerDetail(MCPServerInfo):
    """Detailed MCP server information with endpoints."""

    servers: List[MCPServerEndpoint] = Field(
        default_factory=list, description="Available server endpoints"
    )


class OperationalMCPServer(BaseModel):
    """Operational MCP server with active endpoints."""

    name: str = Field(..., description="Server name")
    id: str = Field(..., description="Server ID")
    description: str = Field(..., description="Server description")
    mcp_servers: List[MCPServerEndpoint] = Field(
        ..., description="Active MCP server endpoints"
    )


class ListServersRequest(BaseModel):
    """Request model for listing MCP servers."""

    filter: Optional[Dict[str, Any]] = Field(
        None,
        description="Filter criteria (category, tag, is_hosted)",
        examples=[{"category": "location-services", "is_hosted": True}],
    )
    total_count: Optional[int] = Field(
        20, ge=1, le=100, description="Number of results to return (1-100)"
    )
    search: Optional[str] = Field(
        "map", description="Search keyword for server name or owner"
    )

    @field_validator("total_count")
    @classmethod
    def validate_total_count(cls, v):
        if v is not None and (v < 1 or v > 100):
            raise ValueError("total_count must be between 1 and 100")
        return v


class GetServerRequest(BaseModel):
    """Request model for getting a specific MCP server."""

    server_id: str = Field(
        "@executeautomation/mcp-playwright",
        description="Server ID in format @group/name or group/name",
    )


class ListOperationalServersRequest(BaseModel):
    """Request model for listing operational MCP servers."""

    pass  # No parameters needed, uses token from header


class ListServersResponse(BaseModel):
    """Response model for listing MCP servers."""

    total_count: int = Field(..., description="Total number of servers found")
    servers: List[MCPServerInfo] = Field(..., description="List of MCP servers")


class ListOperationalServersResponse(BaseModel):
    """Response model for listing operational MCP servers."""

    total_count: int = Field(..., description="Total number of operational servers")
    servers: List[OperationalMCPServer] = Field(
        ..., description="List of operational servers with endpoints"
    )


class GetServerResponse(MCPServerDetail):
    """Response model for getting a specific MCP server."""

    pass


class HealthResponse(BaseModel):
    """Health check response."""

    status: str = Field(..., description="Service status")
    message: str = Field(..., description="Status message")
