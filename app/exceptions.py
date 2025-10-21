class MCPAPIException(Exception):
    """Base exception for MCP API errors."""

    def __init__(self, message: str, detail: str | None = None):
        self.message = message
        self.detail = detail
        super().__init__(self.message)


class AuthenticationError(MCPAPIException):
    """Raised when authentication fails."""

    pass


class ServerNotFoundError(MCPAPIException):
    """Raised when MCP server is not found."""

    pass


class NetworkError(MCPAPIException):
    """Raised when network-related errors occur."""

    pass
