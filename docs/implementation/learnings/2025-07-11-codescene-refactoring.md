# Learning Entry: CodeScene Code Health Failures

**Date**: 2025-07-11  
**Task**: KEY-252 (Leases Tab)  
**Category**: Code Quality, Refactoring

## Issue

PR #24 failed CodeScene code health check after adding leases tab implementation to property detail page.

### Root Cause

The `app/properties/[id]/page.tsx` file grew to **1983 lines** after adding the leases tab functionality. This triggered multiple CodeScene violations:

1. **File Too Large** - Files over ~1000 lines violate the "Lines of Code" metric
2. **Brain Class (God Class)** - Component had too many responsibilities (10+ tabs)
3. **Low Cohesion** - Unrelated features managed in single component

## Solution

### Phase 1: Extract Leases Tab
- Created `components/properties/property-leases-tab.tsx` (361 lines)
- Reduced main file from 1983 to 1667 lines

### Phase 2: Further Decomposition
- Extract `PropertyLeasesStats` (116 lines)
- Extract `PropertyLeasesTable` (131 lines)
- Extract `PropertyDetailHeader` (80 lines)
- Extract `PropertyDetailTabs` (60 lines)
- Reduced `PropertyLeasesTab` from 358 to 189 lines
- Created 6 focused components instead of 2 large ones

## Key Learnings

1. **Monitor File Size During Development**
   - Large files should be refactored immediately
   - Components > 500 lines warrant extraction consideration

2. **CodeScene Metrics to Watch**
   - Brain Method/Class (complexity concentration)
   - Nested Complexity (if-statements inside loops)
   - File size (impacts multiple metrics)

3. **Refactoring Strategies**
   - Extract tab components for multi-tab interfaces
   - Move complex logic to dedicated components
   - Keep parent components as orchestrators only

## Action Items

- [ ] Extract other tabs from property detail page
- [ ] Set up local CodeScene CLI for pre-commit checks
- [ ] Add file size warnings to development guidelines

## Resources

- [CodeScene Code Health Documentation](https://codescene.com/product/code-health)
- [Brain Class Anti-pattern](https://refactoring.guru/smells/large-class) 