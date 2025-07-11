# Day 1: Environment Setup & Core Infrastructure

## Goal
Set up the development environment and core infrastructure for the Autonomous PR System.

## Prerequisites
- Python 3.10+ installed
- PostgreSQL 14+ installed
- Redis 7+ installed
- Git configured
- API keys ready (don't commit them!)

## Step 1: Project Setup

```bash
# Create project directory
mkdir autonomous-pr-system
cd autonomous-pr-system

# Initialize git repository
git init
echo "venv/" >> .gitignore
echo ".env" >> .gitignore
echo "*.log" >> .gitignore
echo "__pycache__/" >> .gitignore

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## Step 2: Install Dependencies

```bash
# Create requirements.txt (or copy from repo)
pip install -r requirements.txt

# Verify installations
python -c "import langgraph; print(f'LangGraph {langgraph.__version__}')"
python -c "import langchain; print(f'LangChain {langchain.__version__}')"
```

## Step 3: Environment Configuration

Create `.env` file:
```bash
# API Keys
OPENAI_API_KEY=sk-...
LANGSMITH_API_KEY=ls-...
LINEAR_API_KEY=lin_api_...
GITHUB_TOKEN=ghp_...

# Database
DATABASE_URL=postgresql://postgres:password@localhost:5432/autonomous_pr
REDIS_URL=redis://localhost:6379

# Configuration
LINEAR_TEAM_ID=your-team-id
GITHUB_REPO=org/repo
VERCEL_PROJECT_ID=prj_...
SENTRY_DSN=https://...

# Safety Settings
MAX_PR_COMPLEXITY=3
REQUIRE_HUMAN_APPROVAL=true
DRY_RUN_MODE=true
```

## Step 4: Database Setup

```sql
-- Create database
CREATE DATABASE autonomous_pr;

-- Connect to database
\c autonomous_pr;

-- Create checkpoints table for LangGraph
CREATE TABLE checkpoints (
    thread_id VARCHAR(255),
    checkpoint_id VARCHAR(255),
    parent_id VARCHAR(255),
    state JSONB,
    metadata JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (thread_id, checkpoint_id)
);

-- Create indexes for performance
CREATE INDEX idx_checkpoints_thread_id ON checkpoints(thread_id);
CREATE INDEX idx_checkpoints_created_at ON checkpoints(created_at);
```

## Step 5: Project Structure

```bash
# Create directory structure
mkdir -p agents/{base,cognitive,production,learning}
mkdir -p graphs/{loops,utils}
mkdir -p integrations/{linear,github,monitoring}
mkdir -p utils/{safety,state}
mkdir -p tests/{unit,integration,e2e}
mkdir -p config
mkdir -p logs

# Create __init__.py files
touch agents/__init__.py
touch agents/base/__init__.py
touch agents/cognitive/__init__.py
touch agents/production/__init__.py
touch agents/learning/__init__.py
touch graphs/__init__.py
touch graphs/loops/__init__.py
touch integrations/__init__.py
touch utils/__init__.py
```

## Step 6: Core Configuration

Create `config/settings.py`:
```python
"""System configuration"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Base paths
BASE_DIR = Path(__file__).parent.parent
LOGS_DIR = BASE_DIR / "logs"

# API Configuration
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4")

# Database
DATABASE_URL = os.getenv("DATABASE_URL")
REDIS_URL = os.getenv("REDIS_URL")

# Safety Settings
MAX_PR_COMPLEXITY = int(os.getenv("MAX_PR_COMPLEXITY", "3"))
REQUIRE_HUMAN_APPROVAL = os.getenv("REQUIRE_HUMAN_APPROVAL", "true").lower() == "true"
DRY_RUN_MODE = os.getenv("DRY_RUN_MODE", "true").lower() == "true"

# Integration Settings
LINEAR_API_KEY = os.getenv("LINEAR_API_KEY")
LINEAR_TEAM_ID = os.getenv("LINEAR_TEAM_ID")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_REPO = os.getenv("GITHUB_REPO")

# Validate required settings
required = ["OPENAI_API_KEY", "LINEAR_API_KEY", "GITHUB_TOKEN", "DATABASE_URL"]
for key in required:
    if not os.getenv(key):
        raise ValueError(f"Missing required environment variable: {key}")
```

## Step 7: Logging Setup

Create `utils/logging.py`:
```python
"""Centralized logging configuration"""
from loguru import logger
import sys
from config.settings import LOGS_DIR

# Remove default handler
logger.remove()

# Console handler with color
logger.add(
    sys.stdout,
    colorize=True,
    format="<green>{time:HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>",
    level="INFO"
)

# File handler for all logs
logger.add(
    LOGS_DIR / "system.log",
    rotation="1 day",
    retention="7 days",
    level="DEBUG",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} - {message}"
)

# File handler for errors only
logger.add(
    LOGS_DIR / "errors.log",
    rotation="1 day",
    retention="30 days",
    level="ERROR",
    format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{line} - {message}\n{exception}"
)

def get_logger(name: str):
    """Get a logger instance for a module"""
    return logger.bind(name=name)
```

## Step 8: Test Setup

Create `tests/conftest.py`:
```python
"""Pytest configuration"""
import pytest
import os
from dotenv import load_dotenv

# Load test environment
load_dotenv(".env.test")

@pytest.fixture
def mock_state():
    """Provide mock cognitive state for testing"""
    return {
        "current_issue": None,
        "current_pr": None,
        "safety_checks": [],
        "execution_log": [],
        "error_log": [],
        "next_action": "idle",
        "cycle_count": 0
    }

@pytest.fixture
def test_config():
    """Provide test configuration"""
    return {
        "dry_run": True,
        "max_complexity": 2,
        "require_approval": True
    }
```

## Step 9: Verify Installation

Create `scripts/verify_setup.py`:
```python
"""Verify environment setup"""
import sys
from utils.logging import get_logger

logger = get_logger(__name__)

def verify_imports():
    """Check all required packages are installed"""
    required_packages = [
        "langgraph",
        "langchain",
        "openai",
        "redis",
        "psycopg2",
        "pydantic",
        "loguru",
        "pytest"
    ]
    
    for package in required_packages:
        try:
            __import__(package)
            logger.success(f"✓ {package} installed")
        except ImportError:
            logger.error(f"✗ {package} missing")
            return False
    return True

def verify_env():
    """Check environment variables"""
    from config.settings import (
        OPENAI_API_KEY, LINEAR_API_KEY, 
        GITHUB_TOKEN, DATABASE_URL
    )
    
    if all([OPENAI_API_KEY, LINEAR_API_KEY, GITHUB_TOKEN, DATABASE_URL]):
        logger.success("✓ All required environment variables set")
        return True
    else:
        logger.error("✗ Missing environment variables")
        return False

def verify_database():
    """Check database connection"""
    try:
        import psycopg2
        from config.settings import DATABASE_URL
        
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()
        cur.execute("SELECT 1")
        cur.close()
        conn.close()
        logger.success("✓ Database connection successful")
        return True
    except Exception as e:
        logger.error(f"✗ Database connection failed: {e}")
        return False

if __name__ == "__main__":
    logger.info("Verifying environment setup...")
    
    checks = [
        ("Imports", verify_imports),
        ("Environment", verify_env),
        ("Database", verify_database)
    ]
    
    all_passed = True
    for name, check in checks:
        if not check():
            all_passed = False
    
    if all_passed:
        logger.success("\n✅ All checks passed! Ready to proceed to Day 2.")
    else:
        logger.error("\n❌ Some checks failed. Please fix before continuing.")
        sys.exit(1)
```

## Step 10: Run Verification

```bash
python scripts/verify_setup.py
```

## Checklist

- [ ] Virtual environment created and activated
- [ ] All dependencies installed
- [ ] Environment variables configured
- [ ] Database created and accessible
- [ ] Project structure created
- [ ] Logging configured
- [ ] Verification script passes

## Next Steps

Once all checks pass, proceed to [Day 2: Base Agent Framework](day-2-agents.md) to build the core agent system. 