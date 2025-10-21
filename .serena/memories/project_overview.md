# Project Overview: modelscope-mcp

## Purpose
A production-ready REST API wrapper for the ModelScope MCP (Model Context Protocol) SDK. This API provides easy-to-use HTTP endpoints to interact with ModelScope's MCP servers.

## Tech Stack
- **Framework**: FastAPI (v0.119.1+)
- **Python**: 3.13+
- **Dependencies**:
  - `modelscope` (v1.31.0+) - Core MCP SDK
  - `pydantic` (v2.12.3+) - Data validation
  - `pydantic-settings` (v2.11.0+) - Settings management
  - `tenacity` (v9.1.2+) - Retry logic
  - FastAPI with standard features (includes uvicorn)

## Key Features
- RESTful API endpoints for MCP server operations
- Automatic retry logic (3 attempts with exponential backoff)
- Comprehensive error handling
- OpenAPI/Swagger documentation
- CORS middleware support
- GZip response compression
- Request timing headers
- Structured logging
- Type safety with Pydantic

## Project Structure
```
modelscope-mcp/
├── app/
│   ├── __init__.py
│   ├── main.py           # FastAPI application entry point
│   ├── routes.py         # API endpoint definitions
│   ├── service.py        # MCP service layer with retry logic
│   ├── models.py         # Pydantic request/response models
│   ├── config.py         # Application configuration
│   └── exceptions.py     # Custom exception classes
├── .env.example          # Environment variable template
├── pyproject.toml        # Project dependencies
├── uv.lock              # Dependency lock file
└── README.md            # Comprehensive documentation
```