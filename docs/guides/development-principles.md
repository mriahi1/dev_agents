# 🏗️ Development Principles

## Core Philosophy

> "A world-class system isn't just well-coded—it's well-organized, observable, and built to last."

## File Organization

### Small, Focused Files

**Principle**: Favor small files grouped by directories with `__init__.py`

```python
# ❌ Bad: large monolithic file
# agents/all_agents.py (2000 lines)

# ✅ Good: organized module structure
agents/
├── __init__.py
├── base/
│   ├── __init__.py
│   ├── agent.py (150 lines)
│   └── state.py (100 lines)
├── cognitive/
│   ├── __init__.py
│   ├── prospect.py (200 lines)
│   ├── user.py (180 lines)
│   └── buyer.py (190 lines)
```

### File Size Guidelines

| Type | Ideal | Maximum | Action if Exceeded |
|------|-------|---------|-------------------|
| Agent Class | 150-200 | 300 | Split into mixins |
| Utility Module | 100-150 | 200 | Create submodules |
| Test File | 200-300 | 400 | Split by feature |
| Config File | 50-100 | 150 | Use includes |

### Directory Structure

Each directory should:
1. Have an `__init__.py` that exports public interface
2. Group related functionality
3. Not exceed 10-15 files (create subdirectories)
4. Include a README.md if complex

Example:
```python
# agents/cognitive/__init__.py
"""Cognitive agents for demand loop"""

from .prospect import ProspectAgent
from .user import UserAgent
from .buyer import BuyerAgent
from .advocate import AdvocateAgent

__all__ = [
    "ProspectAgent",
    "UserAgent", 
    "BuyerAgent",
    "AdvocateAgent"
]
```

## Code Principles

### 1. Durability

Write code that survives:
```python
# ❌ Bad: Hardcoded, brittle
if issue["labels"][0] == "auto-pr-safe":
    process_issue()

# ✅ Good: Defensive, clear
SAFE_LABEL = "auto-pr-safe"
if SAFE_LABEL in issue.get("labels", []):
    process_issue()
```

### 2. Observability

Every action should be traceable:
```python
class BaseAgent:
    def execute(self, state):
        self.logger.info(f"Starting {self.name} execution")
        
        try:
            result = self._execute_internal(state)
            self.log_decision(result)
            return result
        except Exception as e:
            self.logger.error(f"Failed: {e}")
            self.log_error(e, state)
            raise
```

### 3. Composability

Design for swappability:
```python
# ❌ Bad: Tightly coupled
class CreatorAgent:
    def create_pr(self):
        # Directly calls GitHub API
        github.create_pull_request(...)

# ✅ Good: Interface-based
class CreatorAgent:
    def __init__(self, vcs_client: VCSClient):
        self.vcs = vcs_client
    
    def create_pr(self):
        self.vcs.create_pr(...)  # Could be GitHub, GitLab, etc.
```

### 4. Testability

Write testable code:
```python
# ❌ Bad: Hard to test
def process_issue():
    issues = fetch_from_linear()
    for issue in issues:
        if complex_logic(issue):
            create_pr_on_github(issue)

# ✅ Good: Testable
def process_issue(issue_fetcher, pr_creator, validator):
    issues = issue_fetcher.fetch()
    valid_issues = [i for i in issues if validator.is_valid(i)]
    for issue in valid_issues:
        pr_creator.create(issue)
```

### 5. Low Blast Radius

Isolate failures:
```python
class SafetyFirst:
    def execute_with_fallback(self, action, fallback=None):
        try:
            return action()
        except SafetyViolation:
            self.logger.error("Safety violation - stopping")
            raise  # Don't hide safety issues
        except Exception as e:
            self.logger.warning(f"Action failed: {e}")
            if fallback:
                return fallback()
            return None  # Safe default
```

### 6. Expandability

Design for growth:
```python
# Use plugin patterns
class AgentRegistry:
    _agents = {}
    
    @classmethod
    def register(cls, name: str):
        def decorator(agent_class):
            cls._agents[name] = agent_class
            return agent_class
        return decorator
    
    @classmethod
    def create(cls, name: str, **kwargs):
        return cls._agents[name](**kwargs)

# Easy to add new agents
@AgentRegistry.register("prospect")
class ProspectAgent(BaseAgent):
    pass
```

## Testing Patterns

### Test Organization

```
tests/
├── unit/
│   ├── agents/
│   │   ├── test_prospect.py
│   │   └── test_user.py
│   └── utils/
│       └── test_safety.py
├── integration/
│   ├── test_linear_integration.py
│   └── test_github_integration.py
└── e2e/
    └── test_full_cycle.py
```

### Test Principles

1. **Test behavior, not implementation**
2. **Use fixtures for common setup**
3. **Mock external dependencies**
4. **Test edge cases and errors**
5. **Keep tests fast and independent**

## Documentation Standards

### Code Documentation

```python
class ProspectAgent(BaseAgent):
    """Identifies core needs and opportunities.
    
    The Prospect Agent acts as the 'why' identifier in our cognitive
    loop, analyzing signals to find valuable problems to solve.
    
    Attributes:
        pain_threshold: Minimum score to consider a pain point
        learning_rate: How quickly the agent adapts
    
    Example:
        >>> agent = ProspectAgent(pain_threshold=0.7)
        >>> needs = agent.identify_needs(state)
    """
```

### Module Documentation

Each module should have:
1. Purpose statement
2. Key classes/functions
3. Usage examples
4. Dependencies
5. Safety considerations

## Version Control

### Commit Messages

Follow conventional commits:
```
feat(agents): add prospect agent for need identification
fix(safety): prevent auth pattern matching in descriptions  
docs(architecture): explain cognitive loops
test(integration): add Linear API error handling tests
refactor(state): split CognitiveState into smaller types
```

### Pull Request Structure

1. Clear title with type prefix
2. Description of WHY (not just what)
3. Test evidence
4. Safety review checklist
5. Breaking changes noted

## Monitoring & Metrics

### Key Metrics to Track

```python
@dataclass
class AgentMetrics:
    execution_time: float
    decision_count: int
    error_rate: float
    safety_violations: int
    
    def log_to_monitoring(self):
        monitoring.gauge("agent.execution_time", self.execution_time)
        monitoring.counter("agent.decisions", self.decision_count)
        monitoring.gauge("agent.error_rate", self.error_rate)
        monitoring.counter("agent.safety_violations", self.safety_violations)
```

## Evolution Strategy

The system should improve itself:

1. **Collect metrics** on every execution
2. **Analyze patterns** in successes/failures  
3. **Propose improvements** through Evolver agent
4. **Test changes** in safe mode first
5. **Deploy gradually** with rollback capability

---

Remember: We're building cognitive infrastructure that will outlive any individual developer. Make it durable, observable, and beautiful. 