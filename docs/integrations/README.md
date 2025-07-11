# Project Integration Guide - Autonomous PR System

## 🎯 Objective

Configure the autonomous PR system to work on actual projects in the `projects/` directory, creating **high-quality, low-risk pull requests** that can be safely merged.

---

## 📁 Project Structure

```
dev_agents/
├── projects/
│   ├── keysy3/          # Next.js/React frontend application
│   │   ├── app/         # Next.js app directory
│   │   ├── components/  # React components
│   │   ├── lib/         # Utilities and helpers
│   │   └── types/       # TypeScript definitions
│   │
│   └── immo/            # Django backend application
│       ├── apps/        # Django apps (70+ modules)
│       ├── proprio/     # Core Django settings
│       ├── api/         # API documentation
│       └── templates/   # Django templates
│
├── autonomous-pr-system/
│   ├── agents/          # Cognitive agents
│   ├── config/          # Project configurations
│   └── monitoring/      # Deployment tracking
```

---

## 🔧 Multi-Project Configuration

### Project Registry

```python
# config/projects.py
from dataclasses import dataclass
from typing import List, Dict, Optional

@dataclass
class ProjectConfig:
    name: str
    path: str
    type: str  # "frontend" | "backend"
    language: str
    framework: str
    test_command: str
    lint_command: str
    build_command: str
    safe_paths: List[str]  # Paths safe for automation
    unsafe_paths: List[str]  # Never touch these
    pr_template: str
    branch_prefix: str
    
PROJECTS = {
    "keysy3": ProjectConfig(
        name="keysy3",
        path="projects/keysy3",
        type="frontend",
        language="typescript",
        framework="nextjs",
        test_command="npm test",
        lint_command="npm run lint",
        build_command="npm run build",
        safe_paths=[
            "components/ui/",  # UI components are typically safe
            "app/(public)/",   # Public pages
            "lib/utils/",      # Utility functions
            "types/",          # Type definitions
            "docs/",           # Documentation
        ],
        unsafe_paths=[
            "app/api/",        # API routes - critical
            "middleware.ts",   # Auth middleware
            "lib/auth/",       # Authentication logic
            "lib/payments/",   # Payment processing
            ".env*",           # Environment files
        ],
        pr_template="feat(frontend): ",
        branch_prefix="keysy3"
    ),
    
    "immo": ProjectConfig(
        name="immo",
        path="projects/immo",
        type="backend",
        language="python",
        framework="django",
        test_command="python manage.py test",
        lint_command="flake8",
        build_command="python manage.py check",
        safe_paths=[
            "apps/*/templates/",     # Templates are usually safe
            "apps/*/tests/",         # Test files
            "static/",               # Static assets
            "locale/",               # Translations
            "apps/*/serializers.py", # Often safe to modify
            "apps/*/admin.py",       # Admin interface
        ],
        unsafe_paths=[
            "apps/*/migrations/",    # Database migrations
            "apps/billing/",         # Billing logic
            "apps/payments/",        # Payment processing
            "apps/users/auth*",      # Authentication
            "proprio/settings/",     # Core settings
            "apps/*/models.py",      # Database models (careful!)
        ],
        pr_template="feat(backend): ",
        branch_prefix="immo"
    )
}
```

---

## 🛡️ Low-Risk PR Strategy

### 1. Task Classification

```python
class TaskRiskAssessor:
    """Evaluate Linear tasks for automation safety"""
    
    SAFE_TASK_PATTERNS = [
        # UI/UX improvements
        r"(?i)add loading state",
        r"(?i)fix typo",
        r"(?i)update (text|copy|label)",
        r"(?i)improve error message",
        r"(?i)add tooltip",
        
        # Documentation
        r"(?i)document",
        r"(?i)add (readme|docs)",
        r"(?i)update comments",
        
        # Tests
        r"(?i)add (unit |)test",
        r"(?i)increase coverage",
        r"(?i)fix failing test",
        
        # Styling
        r"(?i)fix styling",
        r"(?i)update css",
        r"(?i)responsive design",
        
        # Refactoring (careful)
        r"(?i)extract (function|component)",
        r"(?i)rename variable",
        r"(?i)remove dead code",
    ]
    
    def assess_risk(self, task: LinearTask, project: ProjectConfig) -> RiskLevel:
        """Determine if a task is safe for automation"""
        
        # Check task patterns
        if not any(re.search(pattern, task.title + task.description) 
                  for pattern in self.SAFE_TASK_PATTERNS):
            return RiskLevel.HIGH
        
        # Check affected files
        affected_files = self.predict_affected_files(task, project)
        
        for file in affected_files:
            # Check against unsafe paths
            if any(file.startswith(unsafe) for unsafe in project.unsafe_paths):
                return RiskLevel.HIGH
            
            # Check file type
            if file.endswith(('.sql', '.migration', '.env')):
                return RiskLevel.HIGH
        
        # Check complexity
        if task.estimate and task.estimate > 3:
            return RiskLevel.MEDIUM
        
        return RiskLevel.LOW
```

### 2. Quality Gates

```python
class QualityGateChecker:
    """Ensure PR quality before submission"""
    
    async def check_pr_quality(self, pr: PullRequest, project: ProjectConfig) -> QualityReport:
        checks = []
        
        # 1. Code style
        style_check = await self.run_linter(pr, project)
        checks.append(style_check)
        
        # 2. Tests
        test_check = await self.run_tests(pr, project)
        checks.append(test_check)
        
        # 3. Build
        build_check = await self.run_build(pr, project)
        checks.append(build_check)
        
        # 4. Security
        security_check = await self.run_security_scan(pr, project)
        checks.append(security_check)
        
        # 5. Size limits
        size_check = self.check_pr_size(pr)
        checks.append(size_check)
        
        return QualityReport(
            passed=all(c.passed for c in checks),
            checks=checks,
            risk_score=self.calculate_risk_score(checks)
        )
    
    def check_pr_size(self, pr: PullRequest) -> Check:
        """Ensure PR is small and focused"""
        stats = pr.get_stats()
        
        if stats.files_changed > 5:
            return Check(passed=False, message="Too many files changed")
        
        if stats.lines_added > 200:
            return Check(passed=False, message="Too many lines added")
        
        if stats.lines_deleted > 100:
            return Check(passed=False, message="Too many deletions")
        
        return Check(passed=True, message="PR size is appropriate")
```

---

## 🤖 Project-Aware Agents

### Enhanced Creator Agent

```python
class ProjectAwareCreatorAgent(CreatorAgent):
    """Creates solutions with project context"""
    
    async def execute(self) -> AgentResult:
        task = self.state.current_issue
        
        # 1. Identify target project
        project = await self.identify_project(task)
        if not project:
            return AgentResult(success=False, error="Cannot determine project")
        
        # 2. Load project context
        context = await self.load_project_context(project)
        
        # 3. Generate solution with context
        solution = await self.generate_contextual_solution(task, project, context)
        
        # 4. Validate solution safety
        if not await self.validate_solution_safety(solution, project):
            return AgentResult(success=False, error="Solution touches unsafe areas")
        
        # 5. Create PR
        pr = await self.create_project_pr(solution, project)
        
        return AgentResult(success=True, data={"pr": pr})
    
    async def load_project_context(self, project: ProjectConfig) -> ProjectContext:
        """Load relevant project information"""
        return ProjectContext(
            coding_standards=await self.load_coding_standards(project),
            recent_prs=await self.load_recent_prs(project),
            common_patterns=await self.analyze_code_patterns(project),
            dependencies=await self.load_dependencies(project),
            test_patterns=await self.analyze_test_patterns(project)
        )
    
    async def generate_contextual_solution(self, task, project, context):
        """Generate solution that fits the project style"""
        prompt = f"""
        Project: {project.name} ({project.framework})
        Task: {task.title}
        Description: {task.description}
        
        Project Context:
        - Coding standards: {context.coding_standards}
        - Common patterns in this codebase: {context.common_patterns}
        - Test patterns used: {context.test_patterns}
        
        Generate a solution that:
        1. Follows the existing code style exactly
        2. Uses patterns already present in the codebase
        3. Includes appropriate tests
        4. Is minimal and focused
        5. Has clear commit messages
        
        Focus on safety and quality over cleverness.
        """
        
        return await self.ai_generate_solution(prompt)
```

---

## 📊 Project-Specific Monitoring

### PR Success Tracking

```python
class ProjectPRTracker:
    """Track PR success rates per project"""
    
    def __init__(self):
        self.metrics = defaultdict(lambda: {
            "total_prs": 0,
            "merged": 0,
            "rejected": 0,
            "reverted": 0,
            "avg_review_time": timedelta(),
            "common_issues": Counter()
        })
    
    async def track_pr_outcome(self, pr: PullRequest, project: str, outcome: str):
        """Record PR outcomes for learning"""
        self.metrics[project]["total_prs"] += 1
        self.metrics[project][outcome] += 1
        
        if outcome == "rejected":
            # Learn from rejection
            rejection_reason = await self.analyze_rejection(pr)
            self.metrics[project]["common_issues"][rejection_reason] += 1
            
            # Feed back to Creator agent
            await self.update_creator_knowledge(project, rejection_reason)
    
    def get_project_success_rate(self, project: str) -> float:
        """Calculate success rate for a project"""
        metrics = self.metrics[project]
        if metrics["total_prs"] == 0:
            return 0.0
        
        return metrics["merged"] / metrics["total_prs"]
```

---

## 🚀 Gradual Rollout Plan

### Week 1: Frontend Components (keysy3)
```yaml
targets:
  - UI components (buttons, cards, modals)
  - Loading states and skeletons
  - Error message improvements
  - Tooltip additions
  
constraints:
  - Max 1 component per PR
  - Must include Storybook story
  - Must update tests
  
expected_volume: 3-5 PRs/day
risk_level: LOW
```

### Week 2: Backend Templates & Admin (immo)
```yaml
targets:
  - Django template improvements
  - Admin interface enhancements
  - Static file updates
  - Translation fixes
  
constraints:
  - No model changes
  - No migration files
  - Must test locally first
  
expected_volume: 2-3 PRs/day
risk_level: LOW
```

### Week 3: Test Coverage
```yaml
targets:
  - Missing unit tests
  - Test improvements
  - Test documentation
  
constraints:
  - Only add tests, don't modify code
  - Follow existing test patterns
  - Must increase coverage
  
expected_volume: 3-4 PRs/day
risk_level: VERY LOW
```

### Week 4: Documentation & Types
```yaml
targets:
  - TypeScript type definitions
  - Python type hints
  - README updates
  - API documentation
  
constraints:
  - No logic changes
  - Must be accurate
  - Follow project conventions
  
expected_volume: 4-5 PRs/day
risk_level: VERY LOW
```

---

## 🎯 Success Metrics for Low-Risk PRs

### Quality Indicators
- **Merge Rate**: >90% of PRs merged without changes
- **Review Time**: <30 minutes average review time
- **Revert Rate**: <1% of PRs reverted
- **Build Success**: 100% pass CI/CD
- **Test Coverage**: Maintains or improves coverage

### Risk Indicators
- **Files Changed**: ≤5 files per PR
- **Lines Changed**: ≤200 lines per PR
- **Complexity**: Cyclomatic complexity ≤10
- **Dependencies**: No new dependencies without approval

---

## 🔐 Safety Configuration

```yaml
# config/safety-rules.yaml

global:
  forbidden_files:
    - "*.env*"
    - "*.key"
    - "*.pem"
    - "*secret*"
    - "*/migrations/*"
    - "*/settings/production.py"
  
  forbidden_operations:
    - "DROP"
    - "DELETE FROM"
    - "TRUNCATE"
    - "ALTER TABLE"
    - "stripe."
    - "payment"
    - "billing"
    - "auth"
    - "sudo"
    - "eval("
    - "exec("

per_project:
  keysy3:
    max_file_changes: 5
    max_line_changes: 150
    require_tests: true
    require_types: true
    
  immo:
    max_file_changes: 3
    max_line_changes: 100
    require_tests: true
    require_docstrings: true
```

---

## 📝 PR Template

```markdown
## 🤖 Automated PR

**Linear Issue**: [ISSUE-ID](https://linear.app/team/issue/ISSUE-ID)
**Project**: {{ project_name }}
**Risk Level**: {{ risk_level }}
**Estimated Review Time**: {{ estimate }} minutes

### Changes Made
{{ change_summary }}

### Testing
- [ ] All tests pass
- [ ] Added new tests for changes
- [ ] Manually tested locally
- [ ] No console errors

### Safety Checks
- [ ] No sensitive files modified
- [ ] No authentication/authorization changes
- [ ] No payment/billing logic touched
- [ ] No database migrations needed
- [ ] Changes are reversible

### Screenshots (if UI changes)
{{ screenshots }}

---
*This PR was automatically generated and has passed all quality gates.*
```

---

## 🎯 Getting Started

1. **Configure Projects**
   ```bash
   cp config/projects.example.py config/projects.py
   # Edit with your project specifics
   ```

2. **Set Safety Rules**
   ```bash
   cp config/safety-rules.example.yaml config/safety-rules.yaml
   # Adjust based on your risk tolerance
   ```

3. **Start with Low-Risk Tasks**
   ```bash
   # Run only on documentation tasks first
   python main.py --project keysy3 --task-filter "documentation"
   ```

4. **Monitor Closely**
   ```bash
   # Watch the dashboard
   python -m monitoring.dashboard
   ```

5. **Gradually Increase Scope**
   - Week 1: UI text and styling
   - Week 2: Simple components
   - Week 3: Tests and docs
   - Week 4: Refactoring
   - Week 5+: Feature development

Remember: **Start small, measure everything, and expand gradually!** 