from typing import Optional

from fastapi import APIRouter, Header, HTTPException, status

from app.exceptions import (
    AuthenticationError,
    MCPAPIException,
    ServerNotFoundError,
)
from app.models import (
    GetServerRequest,
    GetServerResponse,
    ListOperationalServersResponse,
    ListServersRequest,
    ListServersResponse,
)
from app.service import MCPService

router = APIRouter(prefix="/api/v1", tags=["MCP Servers"])


def get_service(token: Optional[str] = None) -> MCPService:
    """Get MCP service instance with optional token."""
    return MCPService(token=token)


@router.post(
    "/servers/list",
    response_model=ListServersResponse,
    summary="List MCP Servers",
    description="""
    List available MCP servers with optional filtering and search.

    **Features:**
    - Filter by category, tag, or hosting status
    - Search by server name or owner username
    - Pagination support (1-100 results)
    - Automatic retry on network failures

    **Authentication:**
    - Optional: Providing a token may return more server information
    """,
    responses={
        200: {"description": "Successfully retrieved server list"},
        400: {"description": "Invalid request parameters"},
        500: {"description": "Internal server error"},
    },
)
async def list_servers(
    request: ListServersRequest,
    x_modelscope_token: Optional[str] = Header(
        None, description="ModelScope API token"
    ),
) -> ListServersResponse:
    """List MCP servers with filtering and search capabilities."""
    try:
        service = get_service(token=x_modelscope_token)
        result = service.list_mcp_servers(
            filter_criteria=request.filter,
            total_count=request.total_count or 20,
            search=request.search,
        )
        return ListServersResponse(**result)

    except MCPAPIException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": type(e).__name__,
                "message": e.message,
                "detail": e.detail,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalError",
                "message": "An unexpected error occurred",
                "detail": str(e),
            },
        )


@router.post(
    "/servers/operational",
    response_model=ListOperationalServersResponse,
    summary="List Operational MCP Servers",
    description="""
    List user's activated/deployed MCP servers with endpoint URLs.

    **Features:**
    - Returns only servers the user has activated
    - Includes actual endpoint URLs (SSE, Streamable HTTP)
    - Ready-to-use server configurations

    **Authentication:**
    - Required: Must provide valid ModelScope token in X-Modelscope-Token header
    """,
    responses={
        200: {"description": "Successfully retrieved operational servers"},
        401: {"description": "Authentication required or failed"},
        500: {"description": "Internal server error"},
    },
)
async def list_operational_servers(
    x_modelscope_token: str = Header(
        ..., description="ModelScope API token (required)"
    ),
) -> ListOperationalServersResponse:
    """List operational MCP servers (requires authentication)."""
    try:
        service = get_service(token=x_modelscope_token)
        result = service.list_operational_mcp_servers()
        return ListOperationalServersResponse(**result)

    except AuthenticationError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "AuthenticationError",
                "message": e.message,
                "detail": e.detail,
            },
        )
    except MCPAPIException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": type(e).__name__,
                "message": e.message,
                "detail": e.detail,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalError",
                "message": "An unexpected error occurred",
                "detail": str(e),
            },
        )


@router.post(
    "/servers/detail",
    response_model=GetServerResponse,
    summary="Get MCP Server Details",
    description="""
    Get detailed information about a specific MCP server.

    **Features:**
    - Detailed server configuration and metadata
    - Available endpoint URLs
    - Server capabilities and parameters

    **Server ID Format:**
    - Must be in format: @group/name or group/name
    - Example: @modelscope/ocr-server

    **Authentication:**
    - Optional: May return more details with token
    """,
    responses={
        200: {"description": "Successfully retrieved server details"},
        404: {"description": "Server not found"},
        500: {"description": "Internal server error"},
    },
)
async def get_server(
    request: GetServerRequest,
    x_modelscope_token: Optional[str] = Header(
        None, description="ModelScope API token"
    ),
) -> GetServerResponse:
    """Get detailed information about a specific MCP server."""
    try:
        # Ensure server_id has the @ prefix
        server_id = request.server_id
        if not server_id.startswith("@"):
            server_id = f"@{server_id}"

        service = get_service(token=x_modelscope_token)
        result = service.get_mcp_server(server_id=server_id)
        return GetServerResponse(**result)

    except ServerNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "error": "ServerNotFound",
                "message": e.message,
                "detail": e.detail,
            },
        )
    except MCPAPIException as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": type(e).__name__,
                "message": e.message,
                "detail": e.detail,
            },
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "error": "InternalError",
                "message": "An unexpected error occurred",
                "detail": str(e),
            },
        )
