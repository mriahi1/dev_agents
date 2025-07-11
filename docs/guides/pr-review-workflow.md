# PR Review Workflow with Cursor

A quality-focused workflow for reviewing pull requests using Cursor and the DevOps toolkit.

## Overview

This workflow ensures high-quality code by combining:
- Automated checks via the toolkit
- AI-assisted review with Cursor
- Human oversight for critical decisions

## The Review Process

### 1. Initial Automated Review

Run the toolkit's review command on any PR:

```bash
cursor-toolkit github pr review 21

# Output:
🔍 Reviewing PR #21

✅ Formatting: No issues found
✅ Linting: No linting errors  
❌ Console Logs: Found 2 console.log statements
   → line 145
   → line 203
⚠️ Complexity: Function at line 420 has high cyclomatic complexity (15)
✅ Type Checking: No TypeScript errors

📊 Summary:
   Total issues: 3
   Auto-fixable: 2
   Blocking: 2

❌ This PR has blocking issues that must be resolved before merge.
```

### 2. Cursor-Assisted Deep Review

Ask Cursor to perform a comprehensive review:

```
Review PR #21 for:
1. Logic errors or potential bugs
2. Edge cases not handled
3. Performance implications
4. Security vulnerabilities
5. Accessibility issues
6. Missing error handling
7. Code duplication
8. Test coverage gaps
```

### 3. Auto-Fix Minor Issues

For formatting and simple issues:

```bash
cursor-toolkit github pr review 21 --auto-fix

# Automatically:
# - Fixes formatting
# - Removes console.logs
# - Applies linting fixes
# - Commits changes to PR
```

### 4. Quality Checklist

Before approving any PR, verify:

- [ ] **Functionality**: Does it solve the reported issue?
- [ ] **Code Quality**: Is the code clean and maintainable?
- [ ] **Performance**: No unnecessary re-renders or API calls?
- [ ] **Error Handling**: All edge cases covered?
- [ ] **Security**: No exposed sensitive data?
- [ ] **Tests**: Are there tests for new functionality?
- [ ] **Documentation**: Are complex parts documented?

## Setting Up Automated Checks

### GitHub Actions Integration

Create `.github/workflows/pr-quality.yml`:

```yaml
name: PR Quality Check
on:
  pull_request:
    types: [opened, synchronize]

jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      
      - name: Setup Node
        uses: actions/setup-node@v3
        with:
          node-version: '18'
          
      - name: Install dependencies
        run: npm ci
        
      - name: Type check
        run: npm run type-check
        
      - name: Lint
        run: npm run lint
        
      - name: Format check
        run: npm run format:check
        
      - name: Test
        run: npm test
        
      - name: Check for console.logs
        run: |
          if grep -r "console\.log" --include="*.ts" --include="*.tsx" src/; then
            echo "::error::Found console.log statements"
            exit 1
          fi
```

### Pre-commit Hooks

Use Husky for local checks:

```json
// package.json
{
  "husky": {
    "hooks": {
      "pre-commit": "lint-staged"
    }
  },
  "lint-staged": {
    "*.{ts,tsx}": [
      "eslint --fix",
      "prettier --write",
      "git add"
    ]
  }
}
```

## Best Practices

### 1. Review Early and Often
- Review as soon as the PR is created
- Don't wait until it's "ready" - catch issues early

### 2. Focus on Impact
- Blocking issues: Bugs, security, broken functionality
- Nice-to-have: Style preferences, minor optimizations

### 3. Provide Actionable Feedback
- ❌ "This code is messy"
- ✅ "This function is doing too many things. Consider splitting into `validateInput()` and `processData()`"

### 4. Use the Tools
- Let automation handle formatting/style
- Focus human review on logic and design
- Use Cursor for comprehensive analysis

## Example Review Session

```bash
# 1. Get PR details
cursor-toolkit github pr list --state open

# 2. Run automated review
cursor-toolkit github pr review 21 --json > review.json

# 3. Ask Cursor to analyze
"Analyze the review results in review.json and suggest fixes"

# 4. Apply auto-fixes
cursor-toolkit github pr review 21 --auto-fix

# 5. Update Linear ticket
cursor-toolkit linear update KEY-240 --comment "PR reviewed and approved"
```

## Integration with Linear Workflow

1. When PR is created → Update Linear ticket to "In Review"
2. When review finds issues → Comment on Linear with summary
3. When PR is approved → Update Linear to "Ready to Merge"
4. When PR is merged → Update Linear to "Done"

This ensures complete traceability from task to deployment. 