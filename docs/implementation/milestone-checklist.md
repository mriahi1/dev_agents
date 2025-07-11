# 🎯 Milestone Checklist

## Target Milestone

**A working system that can:**
1. ✅ Read a task from Linear
2. ✅ Implement code changes in the correct project
3. ✅ Create a pull request to staging branch
4. ✅ Update Linear ticket status throughout the process

## Pre-Implementation Checklist

### 1. Type Safety Setup ⚠️
```bash
# Add to requirements.txt
mypy==1.7.1
types-redis==4.6.0
types-psycopg2==2.9.23

# Create mypy.ini
[mypy]
python_version = 3.10
warn_return_any = True
warn_unused_configs = True
disallow_untyped_defs = True
```

### 2. Project Structure 🏗️
```
autonomous-pr-system/
├── src/
│   ├── __init__.py
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── base.py             # BaseAgent with types
│   │   └── production/
│   │       ├── __init__.py
│   │       ├── backlog_reader.py
│   │       ├── safety_checker.py
│   │       ├── creator.py
│   │       └── pr_manager.py
│   ├── integrations/
│   │   ├── __init__.py
│   │   ├── linear.py           # Linear API client
│   │   └── github.py           # GitHub API client
│   ├── graphs/
│   │   ├── __init__.py
│   │   └── production_loop.py  # LangGraph workflow
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── state.py            # State types
│   │   ├── safety.py           # Safety validators
│   │   └── cleanup.py          # Temp file management
│   └── main.py                 # Entry point
├── tests/
│   ├── __init__.py
│   ├── unit/
│   ├── integration/
│   └── fixtures/
├── scripts/
│   ├── setup_db.py
│   └── verify_setup.py
└── Makefile                    # Common commands
```

### 3. Core Components Needed 📦

#### A. Linear Integration
```python
# src/integrations/linear.py
from typing import List, Optional, Dict, Any
from linear_sdk import LinearClient
from pydantic import BaseModel

class LinearTask(BaseModel):
    id: str
    identifier: str
    title: str
    description: str
    state: str
    labels: List[str]
    
class LinearIntegration:
    def __init__(self, api_key: str, team_id: str):
        self.client = LinearClient(api_key)
        self.team_id = team_id
    
    async def get_ready_tasks(self) -> List[LinearTask]:
        """Get tasks marked as ready for automation"""
        
    async def update_task_state(self, task_id: str, state: str) -> bool:
        """Update task workflow state"""
        
    async def add_comment(self, task_id: str, comment: str) -> bool:
        """Add progress comment to task"""
```

#### B. GitHub Integration
```python
# src/integrations/github.py
from typing import Optional, List
from github import Github
from pydantic import BaseModel

class PullRequest(BaseModel):
    number: int
    url: str
    branch: str
    base_branch: str
    
class GitHubIntegration:
    def __init__(self, token: str, repo: str):
        self.github = Github(token)
        self.repo = self.github.get_repo(repo)
    
    async def create_branch(self, branch_name: str, base: str = "staging") -> bool:
        """Create feature branch from staging"""
        
    async def create_pull_request(
        self, 
        title: str,
        body: str,
        branch: str,
        base: str = "staging"
    ) -> PullRequest:
        """Create PR to staging branch"""
        
    async def commit_changes(
        self,
        branch: str,
        files: Dict[str, str],
        message: str
    ) -> bool:
        """Commit file changes"""
```

#### C. State Management
```python
# src/utils/state.py
from typing import TypedDict, Optional, List
from datetime import datetime
from pydantic import BaseModel

class SystemState(TypedDict):
    # Current work
    current_task: Optional[LinearTask]
    current_branch: Optional[str]
    current_pr: Optional[PullRequest]
    
    # Progress tracking
    task_status_updates: List[str]
    files_modified: List[str]
    
    # Safety
    safety_checks_passed: bool
    requires_human_approval: bool
    
    # Cleanup
    temp_files: List[str]
    cleanup_required: bool
```

### 4. Fault Tolerance Patterns 🛡️

#### A. Retry Logic
```python
from tenacity import retry, stop_after_attempt, wait_exponential

class BaseIntegration:
    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=4, max=10)
    )
    async def _make_request(self, *args, **kwargs):
        """Retry failed requests with exponential backoff"""
```

#### B. State Recovery
```python
async def recover_from_incomplete_state(state: SystemState) -> SystemState:
    """Recover from crashes by checking actual state"""
    if state.get("current_branch"):
        # Check if branch still exists
        # Check for uncommitted changes
        # Clean up or resume
```

#### C. Cleanup Manager
```python
# src/utils/cleanup.py
import tempfile
import atexit
from pathlib import Path
from typing import List

class CleanupManager:
    def __init__(self):
        self.temp_files: List[Path] = []
        atexit.register(self.cleanup_all)
    
    def create_temp_file(self, suffix: str = "") -> Path:
        """Create temp file that will be auto-cleaned"""
        
    def cleanup_all(self) -> None:
        """Remove all temporary files"""
```

### 5. Testing Requirements 🧪

#### Unit Tests
```python
# tests/unit/test_linear_integration.py
@pytest.mark.asyncio
async def test_get_ready_tasks_filters_correctly():
    """Should only return tasks with auto-pr-safe label"""

# tests/unit/test_safety_checker.py  
def test_rejects_unsafe_patterns():
    """Should reject tasks with authentication keywords"""
```

#### Integration Tests
```python
# tests/integration/test_full_flow.py
@pytest.mark.integration
async def test_linear_to_pr_flow():
    """Test complete flow from Linear task to GitHub PR"""
```

### 6. Makefile for Easy Use 🚀
```makefile
.PHONY: setup test run clean

setup:
	python -m venv venv
	./venv/bin/pip install -r requirements.txt
	./venv/bin/python scripts/setup_db.py

test:
	./venv/bin/pytest tests/
	./venv/bin/mypy src/

run-dry:
	./venv/bin/python src/main.py --dry-run

run:
	./venv/bin/python src/main.py

clean:
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete
	rm -rf .mypy_cache
```

## Implementation Order 📋

### Phase 1: Core Infrastructure (Day 1-2)
- [ ] Set up project structure
- [ ] Configure type checking
- [ ] Create base classes with proper types
- [ ] Set up logging and error handling
- [ ] Create cleanup manager

### Phase 2: Integrations (Day 3)
- [ ] Linear API client with types
- [ ] GitHub API client with types
- [ ] Test both integrations independently
- [ ] Handle API errors gracefully

### Phase 3: Simple Flow (Day 4-5)
- [ ] BacklogReader agent
- [ ] SafetyChecker agent
- [ ] Basic Creator agent (simple changes only)
- [ ] PR creation logic
- [ ] Linear status updates

### Phase 4: LangGraph Integration (Day 6)
- [ ] Define state transitions
- [ ] Create production loop graph
- [ ] Add checkpointing
- [ ] Test full flow

### Phase 5: Testing & Hardening (Day 7)
- [ ] Unit tests for all components
- [ ] Integration tests
- [ ] Error recovery tests
- [ ] Performance tests
- [ ] Documentation updates

## Success Criteria ✅

### Functionality
- [ ] Successfully reads Linear tasks with correct filters
- [ ] Creates valid Git branches from staging
- [ ] Implements simple code changes (e.g., text updates)
- [ ] Creates PRs with proper description
- [ ] Updates Linear status at each step
- [ ] Handles errors without leaving garbage

### Code Quality  
- [ ] All code has type hints
- [ ] Mypy passes with no errors
- [ ] Test coverage > 80%
- [ ] No hardcoded values
- [ ] Proper error handling throughout

### Maintainability
- [ ] Clear module structure
- [ ] Comprehensive logging
- [ ] Easy configuration via .env
- [ ] Simple CLI interface
- [ ] Clean shutdown handling

## Common Pitfalls to Avoid ⚠️

1. **Don't forget staging branch**: Always target staging, never main
2. **Handle Linear rate limits**: Add delays between API calls
3. **Clean up on failure**: Always remove temp files/branches
4. **Test with small changes first**: Start with README updates
5. **Log everything**: You'll need it for debugging

## Verification Script 🔍

```python
# scripts/verify_milestone.py
async def verify_milestone_ready():
    """Check if system can achieve milestone"""
    checks = {
        "Linear API accessible": check_linear_connection(),
        "GitHub API accessible": check_github_connection(),
        "Can create branches": check_branch_creation(),
        "Can read Linear tasks": check_task_reading(),
        "Database connected": check_db_connection(),
    }
    
    for check, result in checks.items():
        print(f"{'✅' if result else '❌'} {check}")
```

---

## Ready to Start? 🚀

Once all Phase 1-3 items are complete, you'll have a working system that achieves the milestone. The key is to start simple and gradually add complexity while maintaining safety and quality. 