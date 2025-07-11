# Pre-Pull Request Checklist

Use this checklist before creating any pull request to ensure quality and safety.

## 🎯 Branch Strategy
- [ ] Identified the correct base branch (check for `staging`, `develop`, etc.)
- [ ] Verified branch protection rules in repository settings
- [ ] Confirmed PR targets the appropriate branch (NOT `main` unless approved)
- [ ] Used explicit `--base` flag when creating PR

## 🔍 Code Quality
- [ ] Code changes solve the reported issue (verified root cause)
- [ ] No unnecessary files or changes included
- [ ] Followed project coding conventions
- [ ] Added necessary imports and dependencies
- [ ] No console.log or debug statements left

## 📋 Task Alignment
- [ ] Changes align with Linear task description
- [ ] All acceptance criteria addressed
- [ ] Task ID referenced in commit messages
- [ ] Linear task updated to "In Progress"

## 🧪 Testing
- [ ] Tested locally in development environment
- [ ] Verified no breaking changes
- [ ] Tested edge cases mentioned in task
- [ ] Confirmed fix works for the specific reported scenario

## 📝 Documentation
- [ ] PR title follows format: `type(TASK-ID): Brief description`
- [ ] PR description includes:
  - [ ] Problem description
  - [ ] Solution approach
  - [ ] Testing instructions
  - [ ] Screenshots/recordings if UI changes
- [ ] Updated relevant documentation if needed
- [ ] Added comments for complex logic

## 🔒 Security & Safety
- [ ] No hardcoded secrets or API keys
- [ ] Environment variables used appropriately
- [ ] No changes to critical infrastructure without approval
- [ ] Reviewed `/docs/architecture/safety-design.md`

## 🚀 Ready to Create PR?
If all boxes are checked:
```bash
# Example with explicit base branch
gh pr create --base staging --title "feat(KEY-XXX): Description" --body "..."
```

## Post-PR Actions
- [ ] Updated Linear task to "In Review"
- [ ] Added PR link to Linear task
- [ ] Notified relevant stakeholders if needed 