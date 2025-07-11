# Cursor DevOps Toolkit - Source Code

This directory contains the implementation of the Cursor DevOps Toolkit.

## Structure

```
src/
├── main.py              # CLI entry point using Click
├── integrations/        # External service integrations
│   ├── linear_client.py # Linear API client
│   └── github_client.py # GitHub API client
└── utils/              # Shared utilities
    └── types.py        # Type definitions
```

## Architecture

The toolkit follows a simple, modular design:

1. **CLI Interface** (`main.py`)
   - Click-based command structure
   - Groups: `linear`, `github`  
   - JSON output for Cursor parsing

2. **Integration Clients**
   - Each client handles one external service
   - Simple methods that map to API operations
   - Proper error handling and logging

3. **Type Safety**
   - Pydantic models for data validation
   - Type hints throughout
   - Mypy for static checking

## Design Principles

- **Simple** - Each component does one thing well
- **Transparent** - No hidden behavior or "magic"
- **Cursor-Friendly** - Structured output that's easy to parse
- **Extensible** - Easy to add new integrations

## Usage

The toolkit is invoked through the main module:

```bash
python -m src.main [command] [options]
```

See the main [README](../README.md) for usage examples.

## Adding New Integrations

1. Create a new client in `integrations/`
2. Add command group to `main.py`
3. Update environment variables
4. Add tests (when we add testing)

Remember: The toolkit provides operations, Cursor provides intelligence. 