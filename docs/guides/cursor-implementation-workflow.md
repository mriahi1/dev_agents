# Cursor Implementation Workflow - Quick Reference

**Purpose**: Prevent repository confusion and ensure complete PR workflow  
**Use**: Before starting ANY implementation task  
**Status**: 🚨 **MANDATORY** - Follow every time

## 🎯 **Before You Start ANY Implementation**

### ⚠️ **STEP 1: Repository Verification (CRITICAL)**
```bash
# Check where you are
pwd

# Verify repository type
ls -la | head -10
```

### **Decision Tree:**
- **See `package.json`, `app/`, `components/`** → ✅ Frontend repository (correct for React work)
- **See `requirements.txt`, `src/`, `docs/`** → ✅ Toolkit repository (correct for documentation)
- **Unsure?** → 🛑 **STOP** and verify before proceeding

### ⚠️ **STEP 2: Navigate to Correct Repository**
```bash
# For React/UI implementation (components, pages, features):
cd /Users/maximeriahi/Projects/keysy/keysy3

# For documentation, tools, CLI work:
cd /Users/maximeriahi/Projects/dev_agents

# Verify you're in the right place:
pwd && ls -la
```

## 🚀 **Implementation Workflow**

### **STEP 3: Create Feature Branch**
```bash
git checkout main
git pull origin main
git checkout -b feature/KEY-XXX-description
```

### **STEP 4: Implement Feature**
- Create components, pages, or documentation
- Test functionality
- Ensure build passes (`npm run build` for frontend)

### **STEP 5: Complete Commit**
```bash
git add .
git commit -m "feat(KEY-XXX): Clear description of what was implemented"
```

### **STEP 6: Push Branch**
```bash
git push origin feature/KEY-XXX-description
```

### ⚠️ **STEP 7: CREATE PULL REQUEST (CRITICAL)**
```bash
# This step was frequently missed!
gh pr create \
  --title "feat(KEY-XXX): Title" \
  --body "Description of changes" \
  --base main

# Should return: https://github.com/org/repo/pull/XX
```

### **STEP 8: Update Linear**
```bash
cd /Users/maximeriahi/Projects/dev_agents
python -m src.main linear update KEY-XXX \
  --state "In Review" \
  --comment "PR created: [URL] - Ready for review"
```

## 📝 **Repository Quick Reference**

| Task Type | Repository | Path | Indicators |
|-----------|------------|------|------------|
| React Components | `keysy3` | `/Projects/keysy/keysy3` | `package.json`, `app/`, `components/` |
| UI Features | `keysy3` | `/Projects/keysy/keysy3` | Next.js, React dependencies |
| Property Pages | `keysy3` | `/Projects/keysy/keysy3` | Frontend application code |
| Documentation | `dev_agents` | `/Projects/dev_agents` | `docs/`, `requirements.txt` |
| Learning Entries | `dev_agents` | `/Projects/dev_agents` | Python toolkit, CLI tools |
| Linear Tools | `dev_agents` | `/Projects/dev_agents` | `src/`, Python scripts |

## 🚨 **Common Mistakes to Avoid**

### **❌ Repository Confusion**
- Creating React components in `dev_agents`
- Writing documentation in `keysy3`
- Not verifying repository before starting

### **❌ Incomplete PR Workflow**
- Stopping after `git push`
- Forgetting `gh pr create`
- Not updating Linear with PR link

### **❌ Missing Context**
- Assuming which repository you're in
- Not checking `pwd` before starting
- Skipping verification steps

## ✅ **Success Checklist**

After every implementation task:
- [ ] Feature implemented in correct repository
- [ ] Code builds successfully
- [ ] Branch pushed to GitHub
- [ ] **Pull Request created with `gh pr create`**
- [ ] PR URL received and verified
- [ ] Linear task updated with PR link
- [ ] Task status set to "In Review"

## 🔧 **Helper Commands**

### **Repository Check Script**
```bash
# Quick repository verification
if [ -f "package.json" ]; then
  echo "✅ Frontend repository (React/Next.js)"
  echo "  Use for: components, pages, UI features"
elif [ -f "requirements.txt" ]; then
  echo "✅ Toolkit repository (Python/Documentation)"
  echo "  Use for: docs, learning entries, CLI tools"
else
  echo "❌ Unknown repository type - verify before proceeding"
fi
```

### **PR Creation Template**
```bash
gh pr create \
  --title "feat(KEY-XXX): Brief description" \
  --body "## What This PR Does
- Feature 1
- Feature 2

## Technical Changes
- File changes
- New components

## Testing
- Build status
- Manual testing done" \
  --base main
```

## 📞 **When in Doubt**

1. **Stop** and verify repository
2. **Check** what type of work you're doing
3. **Navigate** to correct location
4. **Proceed** with implementation
5. **Complete** full PR workflow

---

**Remember**: 2 minutes of verification saves hours of rework!  
**Goal**: Zero repository confusion, 100% PR creation success 