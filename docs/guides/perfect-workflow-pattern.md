# The Perfect Workflow Pattern

## Overview

This document captures the ideal workflow demonstrated with KEY-250, which represents the perfect synergy between human judgment, Cursor's intelligence, and toolkit operations.

## The Pattern

### 1. Human Creates Issue
- Human identifies a problem or feature need
- Creates issue in Linear with clear description
- Example: "Fix login redirect on Vercel preview links"

### 2. Cursor Takes Ownership
```bash
python -m src.main linear list
```
- Cursor sees available tasks
- Selects appropriate task based on context
- No pattern matching - real understanding

### 3. Cursor Investigates
- Uses native Cursor tools (codebase_search, read_file, grep_search)
- Analyzes actual code to understand the problem
- Forms hypotheses about root causes
- Tests theories by examining more code

### 4. Cursor Implements Solution
- Creates appropriate branch
- Makes targeted changes based on investigation
- Handles edge cases discovered during analysis
- Commits with detailed, meaningful messages

### 5. Cursor Creates PR
```bash
gh pr create --title "..." --body "..." --base staging
```
- Writes comprehensive PR description
- Explains problem, root cause, and solution
- Provides testing instructions
- Links to Linear ticket

### 6. Human Tests & Decides
- Human deploys to preview/staging
- Tests the actual fix
- Makes the merge decision
- Provides feedback if needed

### 7. Cursor Closes Loop
```bash
python -m src.main linear update KEY-250 --state "Done"
```
- Updates Linear to reflect completion
- Ready for next task

## Why This Works

### Clear Separation of Concerns

**Human Responsibilities:**
- Business decisions
- Issue prioritization  
- Quality assurance
- Merge approval

**Cursor Responsibilities:**
- Code analysis
- Problem solving
- Implementation
- Documentation

**Toolkit Responsibilities:**
- Linear operations
- Git operations
- PR creation
- Status updates

### No Automation Theater

- Cursor genuinely understands the code
- Real analysis, not pattern matching
- Transparent operations
- Human maintains control

### Efficient Collaboration

- Human time focused on high-value decisions
- Cursor handles investigation and implementation
- Toolkit provides reliable operations
- Fast iteration cycles

## Applying This Pattern

### For Bug Fixes
1. Human reports bug with reproduction steps
2. Cursor investigates and finds root cause
3. Cursor implements and tests fix
4. Human validates fix works
5. Merge and update status

### For Features
1. Human defines requirements
2. Cursor explores existing patterns
3. Cursor implements following conventions
4. Human reviews implementation
5. Iterate based on feedback

### For Refactoring
1. Human identifies tech debt
2. Cursor analyzes impact
3. Cursor implements incremental changes
4. Human reviews each step
5. Gradual, safe improvement

## Key Insights

1. **Trust Cursor's Intelligence** - It can genuinely understand complex codebases
2. **Keep Toolkit Simple** - Just provide operations, not intelligence
3. **Human Judgment Matters** - Business context and quality decisions need humans
4. **Transparency Builds Trust** - Show what's happening at each step

## Metrics of Success

- Time from issue to PR: < 1 hour for most bugs
- Quality of fixes: Root cause addressed, not symptoms
- PR descriptions: Comprehensive and educational
- Human intervention: Minimal, focused on decisions

## Common Pitfalls to Avoid

1. **Over-automating** - Don't remove human judgment
2. **Under-utilizing Cursor** - Trust it to handle complex analysis
3. **Complex toolkit** - Keep operations simple and composable
4. **Skipping investigation** - Always understand before implementing

## Conclusion

The KEY-250 workflow represents the ideal: Human creativity and judgment combined with Cursor's analytical capabilities, connected by simple, reliable tools. This pattern scales from simple fixes to complex features while maintaining quality and transparency. 