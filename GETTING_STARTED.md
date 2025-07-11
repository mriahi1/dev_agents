# Getting Started with Cursor DevOps Toolkit

Welcome! This toolkit transforms Cursor into a complete development system by providing CLI tools for Linear and GitHub operations.

## Quick Start (5 minutes)

### 1. Install the Toolkit

```bash
# Clone and enter the toolkit
git clone https://github.com/yourusername/cursor-devops-toolkit.git
cd cursor-devops-toolkit

# Create Python environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install toolkit
pip install -e .
```

### 2. Configure Your Environment

```bash
# Copy example config
cp env.example .env

# Edit .env with your credentials:
# - LINEAR_API_KEY: Get from Linear Settings → API → Personal API keys
# - GITHUB_TOKEN: Get from GitHub Settings → Developer settings → Personal access tokens
# - LINEAR_TEAM_ID: Find in Linear URL (linear.app/TEAM_ID/...)
```

### 3. Test Your Setup

```bash
# List Linear tasks
python -m src.main linear list

# You should see your Linear tasks!
```

## Your First Workflow

Let's walk through a real example - fixing a bug:

### Step 1: See What's Available

Ask Cursor: "What Linear tasks are ready to work on?"

Cursor will run:
```bash
python -m src.main linear list
```

### Step 2: Pick a Task

Say you see: `KEY-123: Fix user profile loading bug`

Tell Cursor: "Let's fix KEY-123"

### Step 3: Let Cursor Work

Cursor will:
1. Navigate to the right project
2. Create a branch: `git checkout -b fix/KEY-123-profile-loading`
3. Analyze the codebase to find the bug
4. Implement the fix
5. Commit the changes

### Step 4: Create a PR

Tell Cursor: "Create a PR for this fix"

Cursor will run something like:
```bash
gh pr create --title "Fix user profile loading bug" \
  --body "## Problem\n..." --base main
```

### Step 5: After You Test and Merge

Tell Cursor: "I've merged the PR"

Cursor will update Linear:
```bash
python -m src.main linear update KEY-123 --state "Done"
```

## Multi-Project Setup

If you work on multiple repos, organize like this:

```
workspace/
├── cursor-devops-toolkit/
└── projects/
    ├── frontend/
    ├── backend/
    └── mobile/
```

Then you can work across projects seamlessly!

## Key Commands Reference

### Linear Operations
- `linear list` - Show ready tasks
- `linear create --title "..." --description "..."` - Create task
- `linear update KEY-123 --state "In Progress"` - Update status

### GitHub Operations  
- `github branch feature-name` - Create branch
- `github pr create --title "..." --body "..."` - Create PR

## Tips for Success

1. **Trust Cursor** - It can analyze complex codebases and find real solutions
2. **Be Specific** - "Fix the login bug on Vercel preview" > "Fix login"
3. **Review Changes** - Always review what Cursor implements
4. **Test Everything** - Run the code before merging

## Common Issues

**"No tasks found"**
- Check your LINEAR_TEAM_ID in .env
- Ensure you have tasks in "Ready for Dev" state

**"Authentication failed"**
- Verify your API keys are correct
- Check token permissions (Linear needs read/write, GitHub needs repo access)

**"Command not found"**
- Make sure you've activated the virtual environment
- Run `pip install -e .` again

## Next Steps

1. Read the [Perfect Workflow Pattern](docs/guides/perfect-workflow-pattern.md)
2. Check out [Real Examples](docs/cursor-workflow-examples.md)
3. Start fixing bugs and building features!

## Philosophy

Remember: **Cursor is the brain, this toolkit provides the hands**. You're not automating development - you're empowering Cursor to handle the repetitive DevOps tasks while maintaining full control over the important decisions.

Happy coding! 🚀 