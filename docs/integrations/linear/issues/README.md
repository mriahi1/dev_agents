# Linear Issues Documentation

This directory contains detailed documentation for Linear issues, patterns, and investigation guides.

## Issue Documentation

### Active Issues
- [KEY-252: Leases Tab Empty](./KEY-252-leases-tab-empty.md) - Investigation guide for empty leases tab

### Patterns
- [Empty Tabs Pattern](./empty-tabs-pattern.md) - Common pattern affecting multiple property detail tabs

## Purpose

These documents serve to:
1. **Speed up investigation** - Provide starting points for similar issues
2. **Identify patterns** - Recognize systemic problems across features
3. **Share knowledge** - Help team members learn from past investigations
4. **Prevent regressions** - Document root causes and prevention strategies

## How to Document Issues

When working on a bug, especially one that might be part of a pattern:

1. Create a file: `KEY-XXX-brief-description.md`
2. Include:
   - Problem description
   - Investigation steps
   - Potential root causes
   - Related code locations
   - Testing approach
   - Prevention strategies

3. If you notice a pattern, create a pattern document
4. Link related issues together

## Quick Links

- [Pre-PR Checklist](/docs/implementation/checklists/pre-pr-checklist.md)
- [Learning Protocol](/docs/implementation/learnings/README.md)
- [Linear Workflow](/docs/integrations/linear/workflow.md) 