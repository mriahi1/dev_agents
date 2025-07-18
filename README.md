# Cursor DevOps Toolkit

**Transform Cursor into your DevOps powerhouse** - A CLI toolkit that gives Cursor the ability to manage your entire development workflow.

> **Philosophy**: Cursor is the brain (understands and fixes code), this toolkit provides the hands (executes DevOps operations).

## 🎯 What This Is

A set of CLI tools that Cursor can use to:
- List, create, and update Linear tickets
- Create branches and pull requests
- Manage multi-project workflows
- Execute any DevOps operation you need

## 🚀 Real Workflow Example

Here's what just happened with KEY-250 (a real bug fix):

1. **Human**: "There's a login redirect bug on Vercel preview links" → Creates Linear ticket
2. **Cursor**: Lists available tasks, sees KEY-250
3. **Cursor**: Analyzes the codebase, finds the root cause in cookie domain handling
4. **Cursor**: Implements the fix across multiple files
5. **Cursor**: Creates branch, commits, pushes, opens PR
6. **Human**: Tests on preview deployment, merges PR
7. **Cursor**: Updates Linear ticket to "Done"

**No patterns. No fake AI. Just Cursor's intelligence + simple CLI tools.**

## 🛠 Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/cursor-devops-toolkit.git
cd cursor-devops-toolkit

# Set up Python environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install the toolkit
pip install -e .

# Set up your environment
cp env.example .env
# Edit .env with your API keys and configuration
```

## 🚨 Critical Safety: Repository Verification

**MANDATORY**: Before any coding work, verify you're in the correct repository:

```bash
make verify-repo    # MANDATORY: Run before any file creation
```

**See**: [Repository Verification Integration Guide](docs/implementation/REPOSITORY-VERIFICATION-INTEGRATION.md)

### Quick Commands
- `rc` - Check current repository
- `gk` - Go to keysy3 (React work)
- `gd` - Go to dev_agents (Python work)
- `st <file>` - Safe file creation with verification

## 🔧 Core Commands

### Linear Integration
```bash
# List tasks ready for development
python -m src.main linear list

# Create a new task
python -m src.main linear create --title "Fix navigation bug" --description "..."

# Update task status
python -m src.main linear update KEY-123 --state "In Progress"
```

### GitHub Integration
```bash
# Create a branch
python -m src.main github branch feature/KEY-123-new-feature

# Create a pull request
python -m src.main github pr create \
  --title "Fix login redirect" \
  --body "Detailed description..." \
  --branch fix/KEY-250-login
```

### PR Review

The toolkit includes a comprehensive PR review system that performs real code analysis:

```bash
# Basic code quality review
dev-agents github pr review 123

# Include security analysis
dev-agents github pr review 123 --security

# Include performance analysis
dev-agents github pr review 123 --performance

# Include accessibility analysis
dev-agents github pr review 123 --accessibility

# Full analysis with all checks
dev-agents github pr review 123 --security --performance --accessibility

# Auto-fix formatting issues
dev-agents github pr review 123 --auto-fix

# Get JSON output for parsing
dev-agents github pr review 123 --json
```

The PR review system includes:
- **Code Quality**: Console logs, complexity, TODOs, formatting, linting, TypeScript
- **Security**: Hardcoded secrets, SQL injection, XSS, eval usage, CORS issues
- **Performance**: React re-renders, memoization, bundle size, memory leaks
- **Accessibility**: Alt text, ARIA labels, heading hierarchy, semantic HTML

## 📁 Multi-Project Setup

```
your-workspace/
├── cursor-devops-toolkit/     # This toolkit
├── projects/
│   ├── frontend/             # Your frontend repo
│   ├── backend/              # Your backend repo
│   └── mobile/               # Your mobile repo
```

Configure each project in your `.env`:
```env
FRONTEND_GITHUB_REPO=org/frontend-repo
BACKEND_GITHUB_REPO=org/backend-repo
MOBILE_GITHUB_REPO=org/mobile-repo
```

## 🧠 How Cursor Uses This

In practice, you just tell Cursor what you want:

**You**: "Fix the login redirect bug on Vercel preview links"

**Cursor**:
1. Runs `python -m src.main linear list` to find the ticket
2. Navigates to the project, creates a branch
3. Analyzes the code, implements the fix
4. Creates a PR with detailed explanation
5. Updates Linear when you confirm it's merged

## 🎯 Design Principles

1. **Simple CLI tools** - Each command does one thing well
2. **JSON output** - Easy for Cursor to parse and understand
3. **No magic** - Transparent operations that you could run manually
4. **Extensible** - Add new integrations as needed

## 🔌 Current Integrations

- ✅ **Linear** - Full task management (list, create, update)
- ✅ **GitHub** - Repository operations (branch, PR)
- 🔄 **More coming** - Jira, GitLab, deployment tools

## 🚦 Getting Started

1. **Install the toolkit** (see Installation above)
2. **Configure your API keys** in `.env`
3. **Test the setup**: `python -m src.main linear list`
4. **Start using with Cursor** - Just describe what you want to do!

## 📚 Documentation

- [Workflow Examples](docs/cursor-workflow-examples.md) - See the KEY-250 case study
- [Implementation Guide](docs/implementation/README.md) - Technical details
- [Architecture](docs/architecture/README.md) - System design

## 🤝 Contributing

This toolkit is designed to be extended. Add integrations for:
- Your deployment pipeline
- Your monitoring tools  
- Your communication platform
- Any DevOps tool you use

## 📄 License

MIT License - Use this however you want!

---

**Remember**: This isn't about replacing developers or creating fake automation. It's about giving Cursor the tools to handle the repetitive DevOps tasks so you can focus on what matters - shipping great software. 