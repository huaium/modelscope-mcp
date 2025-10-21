# Task Completion Checklist

When completing a task involving code changes, ensure:

## Code Quality
1. **Type Hints**: All functions have proper type annotations
2. **Docstrings**: Classes and methods have descriptive docstrings
3. **Error Handling**: Appropriate exception handling with custom exceptions
4. **Logging**: Important operations are logged

## Testing
1. Run tests (if they exist): `pytest`
2. Verify no breaking changes

## Code Style
1. **Format code**: `black app/`
2. **Lint code**: `ruff check app/`
3. Follow existing naming conventions

## Documentation
1. Update README.md if adding new features or changing behavior
2. Update docstrings and type hints
3. Ensure OpenAPI docs are accurate (FastAPI auto-generates from code)

## Before Committing
1. Ensure all files use consistent style
2. Check `.env.example` is updated if new config options added
3. Verify no sensitive data (tokens, secrets) in code
4. Test locally: `uvicorn app.main:app --reload`
5. Check health endpoint: `curl http://localhost:8000/health`

## Production Considerations
1. Environment variables properly set in `.env`
2. Log level appropriate for environment
3. CORS origins configured correctly
4. No debug information leaked in production