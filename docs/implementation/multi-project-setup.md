# Multi-Project Setup Guide

The MVP system supports working with multiple projects, each mapped to its own GitHub repository.

## Configuration

### 1. Project Selection

In your `.env` file, specify which project to work on:

```bash
# Choose from available projects in projects/ directory
TARGET_PROJECT=keysy3  # or 'immo'
```

### 2. Repository Mapping

Each project needs its GitHub repository configured:

```bash
# Format: PROJECT_NAME_GITHUB_REPO=owner/repo
KEYSY3_GITHUB_REPO=your-org/keysy3-repo
IMMO_GITHUB_REPO=your-org/immo-repo
```

The system automatically converts the project name to the environment variable:
- `keysy3` → `KEYSY3_GITHUB_REPO`
- `immo` → `IMMO_GITHUB_REPO`  
- `my-project` → `MY_PROJECT_GITHUB_REPO`

### 3. Complete Example

```bash
# API Keys
LINEAR_API_KEY=lin_api_abc123
GITHUB_TOKEN=ghp_xyz789

# Linear Configuration
LINEAR_TEAM_ID=team-123

# Target Project
TARGET_PROJECT=keysy3

# Repository Mappings
KEYSY3_GITHUB_REPO=mycompany/keysy3
IMMO_GITHUB_REPO=mycompany/immo-webapp

# Safety
DRY_RUN_MODE=true
```

## How It Works

1. The system reads `TARGET_PROJECT` from environment
2. Constructs the repo variable name (e.g., `KEYSY3_GITHUB_REPO`)
3. Uses that repository for all GitHub operations
4. Creates PRs to the specified project's repository

## Adding New Projects

1. Create new directory in `projects/`
2. Add mapping in `.env`:
   ```bash
   NEW_PROJECT_GITHUB_REPO=owner/new-project
   ```
3. Set `TARGET_PROJECT=new-project`

## Switching Projects

Simply change `TARGET_PROJECT` in your `.env`:

```bash
# Work on keysy3
TARGET_PROJECT=keysy3

# Later, switch to immo
TARGET_PROJECT=immo
```

No other changes needed - the system automatically uses the correct GitHub repository. 