# Cursor DevOps Toolkit - Workflow Examples

## The Perfect Workflow: KEY-250 Case Study

This documents the ideal workflow demonstrated with KEY-250 (Fix login redirect on Vercel preview links).

### 1. Issue Creation
- Human creates issue in Linear: "Fix login redirect on Vercel preview links"
- Issue gets ID: KEY-250

### 2. Cursor Takes On The Issue
```bash
# List available issues
python -m src.main linear list

# Shows:
📋 KEY-250: Fix login redirect on Vercel preview links
   State: Ready for Dev
```

### 3. Cursor Analyzes The Problem
- Cursor explores the codebase using its native tools
- Reads middleware.ts, AuthContext.tsx, login route
- Identifies root cause: getDomain() setting cookies too broadly for Vercel

### 4. Cursor Implements The Fix
- Creates branch: `git checkout -b fix/KEY-250-vercel-preview-login-redirect`
- Makes targeted code changes:
  - Updates getDomain() in login route
  - Updates client-side TokenService
  - Enhances middleware redirect handling
- Commits with detailed message

### 5. Cursor Creates PR
```bash
# Using gh CLI or toolkit
gh pr create --title "Fix login redirect on Vercel preview links" \
  --body "## Problem\n..." --base staging
```

### 6. Human Tests & Merges
- Human: "I tested preview link and it worked so I merged the pull request"

### 7. Cursor Completes The Loop
```bash
# Update Linear task to Done
python -m src.main linear update KEY-250 --state "Done"
```

## Why This Workflow Is Perfect

1. **Clear Separation of Concerns**
   - Human: Creates issues, tests, makes merge decisions
   - Cursor: Analyzes, implements, handles DevOps
   - Toolkit: Provides the CLI operations

2. **No Fake Automation**
   - Cursor uses its real intelligence to understand and fix bugs
   - No patterns, no pretending
   - Real code analysis and problem-solving

3. **Efficient DevOps**
   - Branch creation, PR creation, and task updates are simple CLI commands
   - Cursor orchestrates these commands as part of the workflow

## Standard Workflow Template

### For Bug Fixes
1. `python -m src.main linear list` - Find the issue
2. Create branch in the project directory
3. Cursor analyzes and implements fix
4. Create PR with detailed explanation
5. Human tests on preview/staging
6. After merge: `python -m src.main linear update [TASK-ID] --state "Done"`

### For Feature Development
1. `python -m src.main linear create` - Create task if needed
2. Create feature branch
3. Cursor implements feature following existing patterns
4. Create PR with implementation details
5. Human reviews and tests
6. Update Linear task through states: "In Progress" → "In Review" → "Done"

### For Quick Updates
1. Direct to branch and implement
2. Create PR with context
3. Quick review and merge

## Multi-Project Considerations

When working across multiple projects:
```bash
# Navigate to specific project
cd projects/keysy3
# or
cd projects/backend

# Work within that project's context
git checkout -b feature/...
# Make changes
gh pr create ...
```

## Key Principles

1. **Cursor is the brain** - It understands code, finds bugs, implements solutions
2. **Toolkit provides the hands** - Simple CLI commands for DevOps operations
3. **Human provides judgment** - Tests, approves, makes business decisions
4. **No automation theater** - Everything is transparent and real

This workflow scales from simple typo fixes to complex bug investigations, always maintaining the same clear pattern. 