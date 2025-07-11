# Integrations Guide

This directory contains documentation for integrating external services with the Cursor DevOps Toolkit.

## Current Integrations

### Linear
- API client for task management
- Commands: list, create, update tasks
- See [Linear Workflow](linear/workflow.md)

### GitHub  
- API client for repository operations
- Commands: create branches, create PRs
- Direct integration via PyGithub

## Adding New Integrations

To add a new service integration:

1. **Create the client** in `src/integrations/`
   ```python
   class ServiceClient:
       def __init__(self, api_key: str):
           # Initialize connection
   ```

2. **Add commands** to `src/main.py`
   ```python
   @cli.group()
   def service():
       """Service operations"""
       pass
   ```

3. **Update environment** in `env.example`
   ```
   SERVICE_API_KEY=your_key_here
   ```

4. **Document usage** in this directory

## Integration Principles

- **Simple methods** - One method per API operation
- **Error handling** - Graceful failures with clear messages
- **Logging** - Use loguru for consistent logging
- **Type safety** - Pydantic models for data validation

## Future Integrations

Potential services to integrate:
- Jira (alternative to Linear)
- GitLab (alternative to GitHub)
- Slack (notifications)
- PagerDuty (incident management)
- Vercel/Netlify (deployment status) 