# AGENTS.md - Guide for AI Coding Agents

This document provides guidance for AI coding agents (Claude, Cursor, Windsurf, Copilot, etc.) working on the ModelScope MCP REST API project.

## Project Overview

**ModelScope MCP REST API** is a FastAPI-based REST API wrapper for the ModelScope MCP (Model Context Protocol) SDK. It provides HTTP endpoints to interact with ModelScope's AI agent capabilities.

### Technology Stack

- **Framework**: FastAPI (v0.119.1+)
- **Python**: >=3.13
- **Key Dependencies**:
  - `modelscope` (>=1.31.0) - Core MCP SDK
  - `pydantic` (>=2.12.3) - Data validation
  - `tenacity` (>=9.1.2) - Retry logic
  - `uvicorn` - ASGI server

### Project Structure

```
modelscope-mcp/
├── app/
│   ├── __init__.py
│   ├── config.py        # Application configuration
│   ├── exceptions.py    # Custom exceptions
│   ├── models.py        # Pydantic models
│   ├── routes.py        # API route handlers
│   └── service.py       # Business logic & MCP integration
├── main.py              # Application entry point
├── pyproject.toml       # Project dependencies
├── .env.example         # Environment variable template
└── README.md            # Project documentation
```

## Development Guidelines

### 1. Code Style & Conventions

#### Python Style

- Follow **PEP 8** conventions
- Use **type hints** for all function parameters and return values
- Document functions with **docstrings** (Google style preferred)
- Use **async/await** for I/O operations
- Keep functions focused and single-purpose

#### Naming Conventions

- Classes: `PascalCase` (e.g., `MCPAPIException`)
- Functions/Methods: `snake_case` (e.g., `get_settings`)
- Constants: `UPPER_SNAKE_CASE` (e.g., `DEFAULT_TIMEOUT`)
- Private methods: `_leading_underscore` (e.g., `_internal_method`)

#### Import Organization

1. Standard library imports
2. Third-party imports
3. Local application imports

```python
import logging
import sys
from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from pydantic import BaseModel

from app.config import get_settings
from app.models import HealthResponse
```

### 2. Architecture Patterns

#### Layered Architecture

- **main.py**: Application setup, middleware, exception handlers
- **routes.py**: HTTP endpoint definitions (thin controllers)
- **service.py**: Business logic and external service integration
- **models.py**: Request/response schemas and data models
- **config.py**: Configuration management
- **exceptions.py**: Custom exception definitions

#### Dependency Injection

- Use FastAPI's dependency injection system
- Singleton pattern for settings: `get_settings()`
- Keep dependencies explicit and testable

#### Error Handling

- Use custom exceptions from `exceptions.py`
- Implement global exception handlers in `main.py`
- Log errors with appropriate severity levels
- Return meaningful error messages to clients

### 3. Configuration Management

#### Environment Variables

- Use `.env` file for local development (not committed)
- Reference `.env.example` for required variables
- Use `pydantic-settings` for validation
- Access via `get_settings()` singleton

#### Key Configuration Areas

- **Logging**: Configurable log levels (DEBUG, INFO, WARNING, ERROR)
- **CORS**: Allowed origins for cross-origin requests
- **API Settings**: Timeouts, retry policies, etc.

### 4. API Design Principles

#### RESTful Conventions

- Use appropriate HTTP methods (GET, POST, PUT, DELETE)
- Return proper status codes (200, 201, 400, 404, 500)
- Use plural nouns for resource endpoints
- Version API if needed (`/v1/...`)

#### Request/Response Models

- Define Pydantic models for all request bodies
- Define response models for type safety
- Use `response_model` parameter in route decorators
- Include examples in model definitions

#### Endpoint Documentation

- Add `tags` for grouping in Swagger UI
- Write clear `summary` and `description`
- Document parameters and responses
- Include usage examples

### 5. Testing Considerations

#### Test Structure (when adding tests)

```
tests/
├── test_routes.py       # API endpoint tests
├── test_service.py      # Business logic tests
├── test_models.py       # Model validation tests
└── conftest.py          # Pytest fixtures
```

#### Testing Best Practices

- Use `pytest` for testing framework
- Use `httpx` for async HTTP client tests
- Mock external dependencies (ModelScope SDK)
- Test both success and error scenarios
- Aim for >80% code coverage

### 6. Logging & Monitoring

#### Logging Strategy

- Use structured logging with contextual information
- Log levels:
  - **DEBUG**: Detailed debugging information
  - **INFO**: General informational messages, request/response logs
  - **WARNING**: Validation errors, retryable failures
  - **ERROR**: Unhandled exceptions, critical failures

#### Request Logging

- Log all incoming requests with method and path
- Include response status and processing time
- Add `X-Process-Time` header to responses

### 7. Performance Optimization

#### Middleware

- **CORS**: Configured for allowed origins
- **GZip**: Compression for responses >1000 bytes
- **Request Logging**: Minimal overhead tracking

#### Best Practices

- Use async operations for I/O-bound tasks
- Implement connection pooling for external services
- Use retry logic with exponential backoff (via `tenacity`)
- Cache configuration and settings

### 8. Security Considerations

#### Input Validation

- Use Pydantic models for automatic validation
- Sanitize user inputs
- Validate file uploads (if applicable)
- Set request size limits

#### CORS Configuration

- Define explicit allowed origins
- Don't use `allow_origins=["*"]` in production
- Configure allowed methods and headers appropriately

#### Error Handling

- Don't expose internal errors in production
- Use DEBUG mode only for development
- Log sensitive errors server-side only

### 9. Agent-Specific Workflow

#### When Adding New Features

1. **Understand Requirements**: Read existing code and documentation
2. **Check Configuration**: Review `config.py` and `.env.example`
3. **Define Models**: Create Pydantic models in `models.py`
4. **Implement Service Logic**: Add business logic to `service.py`
5. **Create Routes**: Add endpoints in `routes.py`
6. **Update Documentation**: Add docstrings and API descriptions
7. **Test Manually**: Use `/docs` endpoint for interactive testing

#### When Fixing Bugs

1. **Reproduce**: Understand the error from logs/description
2. **Locate**: Find relevant code in appropriate layer
3. **Fix**: Make minimal, focused changes
4. **Verify**: Check related functionality isn't broken
5. **Log**: Ensure proper error logging is in place

#### When Refactoring

1. **Identify**: Find code smells or improvement opportunities
2. **Plan**: Consider impact on other components
3. **Maintain**: Keep backward compatibility where possible
4. **Document**: Update docstrings and comments
5. **Test**: Verify all functionality still works

### 10. Common Tasks

#### Adding a New Endpoint

```python
# 1. Define request/response models in models.py
class MyRequest(BaseModel):
    field: str

class MyResponse(BaseModel):
    result: str

# 2. Implement service logic in service.py
async def process_my_request(data: MyRequest) -> MyResponse:
    # Business logic here
    return MyResponse(result="processed")

# 3. Add route in routes.py
@router.post("/my-endpoint", response_model=MyResponse)
async def my_endpoint(request: MyRequest):
    return await process_my_request(request)
```

#### Adding Configuration

```python
# 1. Add to config.py Settings class
class Settings(BaseSettings):
    new_setting: str = "default_value"

# 2. Add to .env.example
NEW_SETTING=example_value

# 3. Use in code
settings = get_settings()
value = settings.new_setting
```

#### Custom Exception

```python
# 1. Define in exceptions.py
class MyCustomException(MCPAPIException):
    def __init__(self, message: str, detail: dict | None = None):
        super().__init__(message, detail)

# 2. Use in service code
raise MyCustomException("Error occurred", {"context": "details"})
```

## Quick Reference

### Running the Application

```bash
# Development mode with auto-reload
python main.py

# Or using uvicorn directly
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Key Endpoints

- **`/`** - API information and links
- **`/health`** - Health check
- **`/docs`** - Interactive Swagger UI
- **`/redoc`** - ReDoc documentation
- **`/openapi.json`** - OpenAPI schema

### Environment Setup

```bash
# Install dependencies (using uv)
uv pip install -e .

# Copy environment template
cp .env.example .env

# Edit .env with your configuration
```

## Resources

- **FastAPI Documentation**: https://fastapi.tiangolo.com/
- **Pydantic Documentation**: https://docs.pydantic.dev/
- **ModelScope**: https://www.modelscope.cn/
- **Python Type Hints**: https://docs.python.org/3/library/typing.html

## Notes for Agents

- Always check existing code patterns before implementing new features
- Maintain consistency with established conventions
- Ask for clarification on ambiguous requirements
- Test changes using the `/docs` interactive API
- Keep security and error handling in mind
- Update this document when introducing new patterns or conventions
