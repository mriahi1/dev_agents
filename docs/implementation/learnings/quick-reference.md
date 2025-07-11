# Learning System Quick Reference

## 🚀 After Each Task

1. **Create Learning Entry**
   ```bash
   docs/implementation/learnings/YYYY-MM-DD-TASK-ID.md
   ```

2. **Answer Key Questions**
   - What was the intended outcome?
   - What actually happened?
   - Why did issues occur?
   - What would I do differently?

3. **Extract Rules**
   - Turn insights into actionable rules
   - Update checklists and documentation
   - Add to improvement-actions.md if systemic

## 🎯 Key Learnings So Far

### Always Check Branch Strategy
```bash
# Before any PR:
git branch -r | grep -E "(staging|develop)"
gh pr create --base staging  # Explicit base!
```

### Follow the Workflow
1. Linear → In Progress
2. Branch → Implement  
3. Checklist → PR to staging
4. Linear → In Review
5. Document → Learn

### Verify Root Cause
- Reproduce issue first
- Test in reported environment
- Include evidence in PR

## 📋 Essential Checklists

- **Pre-PR**: `/docs/implementation/checklists/pre-pr-checklist.md`
- **Safety**: `/docs/architecture/safety-design.md`
- **Conventions**: `/docs/guides/development-principles.md`

## 🔄 Continuous Improvement

**Every Task**: Create learning entry
**Every Week**: Review entries for patterns  
**Every Month**: Update processes
**Every Quarter**: Measure improvement

## 💡 Remember

> "The best mistake is one that becomes a learning that prevents all future similar mistakes."

The goal isn't perfection—it's systematic improvement through documented learning. 