# 🚨 CRITICAL WORKFLOW CHECKLIST

**Status**: 🚨 **MANDATORY** - Use before EVERY implementation task  
**Purpose**: Prevent repository confusion and incomplete PR workflows  
**Time**: 2 minutes - saves hours of rework

## ⚠️ **PRE-IMPLEMENTATION VERIFICATION**

### **Step 1: Repository Check**
```bash
pwd && ls -la | head -5
```

**Decision Matrix**:
- ✅ See `package.json` + `app/` + `components/` → Frontend work (React/UI)
- ✅ See `requirements.txt` + `src/` + `docs/` → Toolkit work (Documentation/CLI)
- 🛑 Unsure? **STOP** and verify before proceeding

### **Step 2: Navigation**
```bash
# For React/UI implementation:
cd /Users/maximeriahi/Projects/keysy/keysy3

# For documentation/tools:
cd /Users/maximeriahi/Projects/dev_agents

# Verify correct location:
pwd
```

## ✅ **COMPLETE IMPLEMENTATION WORKFLOW**

### **Development**
- [ ] Create feature branch
- [ ] Implement feature in correct repository
- [ ] Test functionality/build

### **Commit & Push**
- [ ] `git add .`
- [ ] `git commit -m "feat(KEY-XXX): Description"`
- [ ] `git push origin feature/branch-name`

### **⚠️ PR CREATION (CRITICAL)**
- [ ] **`gh pr create --title "..." --body "..." --base main`**
- [ ] Verify PR URL returned
- [ ] Copy PR URL for Linear update

### **Linear Update**
- [ ] Navigate to dev_agents if needed
- [ ] `python -m src.main linear update KEY-XXX --state "In Review" --comment "PR created: [URL]"`

## 🚨 **COMMON FAILURES TO AVOID**

- ❌ **Creating React components in dev_agents**
- ❌ **Stopping after git push without creating PR**
- ❌ **Assuming repository without verification**
- ❌ **Not updating Linear with PR link**

## 🎯 **SUCCESS CRITERIA**

Task is complete ONLY when:
- ✅ Feature implemented in correct repository
- ✅ PR created and URL obtained
- ✅ Linear updated with PR link
- ✅ Status set to "In Review"

---

**Remember**: Verification takes 2 minutes, fixes take hours! 