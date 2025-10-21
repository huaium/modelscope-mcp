# Suggested Commands

## Installation
```bash
# Using uv (recommended)
uv sync

# Using pip
pip install -e .
```

## Running the Application

### Development Mode
```bash
# Using uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Using Python module
python -m app.main

# Running main.py directly (runs on port 9000)
python main.py
```

### Production Mode
```bash
# Without reload
uvicorn app.main:app --host 0.0.0.0 --port 8000
```

## Configuration
```bash
# Create .env file from example
cp .env.example .env
```

## Development Tools

### Code Formatting (Mentioned in README)
```bash
black app/
```

### Linting (Mentioned in README)
```bash
ruff check app/
```

### Testing (Mentioned in README)
```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest
```

## System Commands (macOS)
- `ls` - List directory contents
- `cd` - Change directory
- `cat` - Display file contents
- `grep` - Search text
- `find` - Find files
- `git` - Version control

## API Access
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc
- Health Check: http://localhost:8000/health