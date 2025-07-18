# System Improvement Actions

This document tracks concrete actions derived from learning entries to improve the system.

## Active Improvements

### 1. Automated Branch Protection Checks
**Source**: [2025-07-11-KEY-251](./2025-07-11-KEY-251.md)
**Status**: 🔄 In Progress
**Description**: Create automated validation for PR base branches

**Implementation**:
```bash
# Add to .github/pre-commit or as git hook
#!/bin/bash
# Check if PR targets staging first
if [[ "$BASE_BRANCH" == "main" || "$BASE_BRANCH" == "master" ]]; then
  echo "⚠️  WARNING: PRs should target 'staging' branch first!"
  echo "Use: gh pr create --base staging"
  read -p "Continue anyway? (y/N) " -n 1 -r
  echo
  if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    exit 1
  fi
fi
```

### 2. Task Implementation Workflow
**Source**: [2025-07-11-KEY-251](./2025-07-11-KEY-251.md)
**Status**: ✅ Documented
**Description**: Formalize the successful workflow pattern

**Standard Workflow**:
1. Create/claim Linear task
2. Update status to "In Progress"
3. Create feature branch
4. Implement changes
5. Run pre-PR checklist
6. Create PR to staging
7. Update Linear to "In Review"
8. Document learnings

### 3. Root Cause Verification Protocol
**Source**: [2025-07-11-KEY-251](./2025-07-11-KEY-251.md) (PR #21 investigation)
**Status**: 📋 Planned
**Description**: Ensure fixes address actual problems

**Protocol**:
1. Reproduce the issue locally
2. Verify issue exists in reported environment
3. Identify root cause with evidence
4. Test fix in same environment as report
5. Include reproduction steps in PR

### 4. Bug Report Verification Template
**Source**: [2025-07-11-KEY-252](./2025-07-11-KEY-252.md)
**Status**: 🔄 In Progress
**Description**: Improve bug reports to avoid miscommunication

**Template Addition**:
```markdown
## Bug Report Checklist
- [ ] Feature/Component exists in the UI
- [ ] I can navigate to the feature
- [ ] The issue is not that the feature is missing
- [ ] Exact error or behavior described
- [ ] Steps to reproduce included
- [ ] Environment specified (local/preview/staging)
```

**Why**: KEY-252 was reported as "empty tab" but the tab didn't exist at all.

### 5. UI Feature Audit
**Source**: [2025-07-11-KEY-252](./2025-07-11-KEY-252.md)
**Status**: 📋 Planned
**Description**: Audit property detail page for other missing tabs

**Action Items**:
- [ ] List all data hooks that exist
- [ ] Check which ones have UI implementations
- [ ] Create tasks for missing UI components
- [ ] Ensure data layer and UI layer are in sync

### 6. CodeScene Integration
**Source**: [2025-07-11-codescene-refactoring](./2025-07-11-codescene-refactoring.md)
**Status**: 🔄 In Progress
**Description**: Integrate CodeScene checks into development workflow

**Action Items**:
- [ ] Set up CodeScene CLI for local development
- [ ] Add pre-commit hooks for code health checks
- [ ] Extract remaining tabs from property detail page (1667 lines → <1000)
- [ ] Create file size guidelines in development docs
- [ ] Monitor CodeScene metrics in PR reviews

**Key Metrics to Watch**:
- File size (aim for <500 lines per component)
- Brain Class detection
- Nested complexity
- Low cohesion warnings

### 7. React Hook Best Practices
**Source**: [2025-07-11-infinite-loop-fix](./2025-07-11-infinite-loop-fix.md)
**Status**: 📋 Planned
**Description**: Establish patterns to prevent infinite loops and performance issues

**Action Items**:
- [ ] Document hook dependency best practices
- [ ] Create custom hook guidelines
- [ ] Add ESLint rules for exhaustive-deps
- [ ] Review existing hooks for similar issues
- [ ] Create useMemo/useCallback usage guide

**Pattern Library**:
```typescript
// Document common patterns
- Static initial values
- Proper update methods
- Dependency optimization
```

### 8. API Terminology Standardization
**Source**: [2025-07-11-api-terminology](./2025-07-11-api-terminology.md)
**Status**: 📋 Planned
**Description**: Document and standardize frontend/backend terminology differences

**Action Items**:
- [ ] Create API terminology mapping document
- [ ] Build translation constants file (e.g., API_TERMS.ts)
- [ ] Update all API service files with clear comments
- [ ] Consider refactoring to use consistent terms
- [ ] Add to onboarding documentation

**Known Mappings**:
- Frontend: `property` → Backend: `operation`
- Frontend: `propertyId` → API param: `operation`
- Lease object: `lease.operation` (not `lease.property`)

## Completed Improvements

### Learning Protocol System
**Completed**: 2025-07-11
**Impact**: Systematic capture of insights for continuous improvement
- Created learning entry template
- Established meta-learning process
- Set up improvement tracking

## Metrics to Track

1. **Branch Strategy Compliance**
   - PRs to staging vs main ratio
   - Time to catch branching errors

2. **Fix Effectiveness**
   - Issues reopened after "fix"
   - Root cause identification accuracy

3. **Process Efficiency**
   - Time from task start to PR
   - Linear status update compliance

## Review Schedule

- **Weekly**: Review new learning entries
- **Monthly**: Update improvement actions
- **Quarterly**: Analyze metrics and adjust processes 