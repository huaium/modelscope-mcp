# Code Style and Conventions

## Python Version
- Requires Python 3.13+

## Code Style
- **Type Hints**: Full type annotations using modern Python syntax (e.g., `list[str]`, `dict[str, Any]`)
- **Docstrings**: Google-style docstrings for classes and methods
- **Imports**: Standard library → Third-party → Local imports
- **String Quotes**: Double quotes for strings

## Naming Conventions
- **Classes**: PascalCase (e.g., `MCPService`, `ListServersRequest`)
- **Functions/Methods**: snake_case (e.g., `list_mcp_servers`, `get_service`)
- **Constants**: UPPER_SNAKE_CASE (would be used for constants)
- **Private attributes**: Single underscore prefix (e.g., `_api`)

## Code Organization
- **Separation of Concerns**: 
  - `routes.py` - API endpoint definitions
  - `service.py` - Business logic with error handling
  - `models.py` - Data validation schemas
  - `config.py` - Configuration management
  - `exceptions.py` - Custom exceptions
  - `main.py` - Application setup, middleware, global handlers

## Error Handling
- Custom exception hierarchy inheriting from `MCPAPIException`
- Specific exceptions: `AuthenticationError`, `ServerNotFoundError`, `RequestValidationError`, `NetworkError`
- Retry logic using `tenacity` library for network operations
- Comprehensive error logging

## Dependency Injection
- Settings via `get_settings()` with `@lru_cache`
- Service instances via factory functions

## Async/Await
- All route handlers are async functions
- Consistent use of `async def` for FastAPI endpoints

## Logging
- Structured logging with log levels
- Request/response logging via middleware
- Error logging in service layer