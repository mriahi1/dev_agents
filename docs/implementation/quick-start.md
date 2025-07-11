# 🚀 Autonomous PR System - Quick Start Guide

## What This System Does

An **autonomous engineering organization in a box** powered by **LangGraph** that:

1. **Knows WHY it builds** - Identifies real needs through cognitive demand loop
2. **Knows WHAT to build** - Selects valuable work from Linear backlog
3. **Knows HOW to build** - Creates, refines, and deploys code autonomously  
4. **Learns and evolves** - Gets better with every cycle through feedback

This is not just automation - it's a **self-aware, self-improving colleague** built on LangGraph's stateful orchestration that mimics the cognitive structure of a real product organization.

## 🔒 Safety First

### Branch Protection
- ❌ **NEVER** push to: `main`, `master`, `staging`, `production`, `prod`
- ❌ **NEVER** merge pull requests to main or production
- ✅ **ONLY** work on feature branches (format: `auto/issue-id`)
- ✅ **ALWAYS** check branch name before any git operations

### Code Safety
- ❌ **NEVER** delete production code without explicit confirmation
- ❌ **NEVER** modify critical infrastructure files (`.env`, `docker-compose.yml`)
- ❌ **NEVER** expose secrets, API keys, or credentials
- ❌ **NEVER** touch auth, payments, or database schemas
- ✅ **ALWAYS** validate inputs and handle edge cases defensively
- ✅ **ALWAYS** monitors deployment health

### User Issue Protection  
- ❌ **NEVER** modify user-created issues without explicit permission
- ✅ **ALWAYS** identify AI-generated vs user-created issues
- ✅ **REQUIRE** clear AI markers on all agent-created issues
- ✅ **DEFAULT** to protection when issue origin is unclear

### Safe Issue Types
1. UI text/typos
2. Adding tests
3. Documentation
4. Minor dependency updates
5. Simple bug fixes with clear scope

## 📦 Setup in 5 Minutes

```bash
# 1. Clone and setup
git clone <your-repo>
cd autonomous-pr-system
python -m venv venv
source venv/bin/activate

# 2. Install dependencies (including LangGraph)
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your API keys

# 4. Test connection
python -m agents.test_connections

# 5. Run in shadow mode
python main.py --shadow-mode
```

## 🧠 The Cognitive Agents (Powered by LangGraph)

LangGraph orchestrates three cognitive loops that work together:

### Demand Loop (Intent Formation)
- **Prospect Agent** - "Why do I care?" - Identifies core needs
- **User Agent** - "How do I try it?" - Explores solutions
- **Buyer Agent** - "Is it worth it?" - Evaluates ROI
- **Advocate Agent** - "Is it worth sharing?" - Amplifies value

### Production Loop (Execution)
- **Creator Agent** - Writes initial solutions with creative freedom
- **Editor Agent** - Refines code to production standards
- **Reviewer Agent** - Quality gate and approval
- **Merger Agent** - Safe deployment to staging

### Learning Loop (Evolution)
- **Analyst Agent** - Observes outcomes and generates insights
- **Feedback** - Updates all agents to improve over time

The entire system uses LangGraph's state management, checkpointing, and human-in-the-loop capabilities for safe, reliable operation.

## 🔑 Required API Keys

| Service | Purpose | Get it from |
|---------|---------|-------------|
| Linear | Read/update issues | https://linear.app/settings/api |
| GitHub | Create PRs | https://github.com/settings/tokens |
| OpenAI | Generate code | https://platform.openai.com |
| Vercel | Monitor deployments | https://vercel.com/account/tokens |
| Sentry | Track errors | https://sentry.io/settings/auth-tokens |

## 🏃 Running the System

### Shadow Mode (Recommended First)
```bash
# Logs decisions without taking action
python main.py --shadow-mode --days 2
```

### Limited Mode
```bash
# Process max 1 issue per day
python main.py --limit 1 --max-complexity 2
```

### Full Mode
```bash
# Run with all safety checks
python main.py
```

## 📊 Monitor Progress

### CLI Commands
```bash
# Check system status
./agent status

# View recent activity
./agent logs --tail 50

# Pause automation
./agent pause --reason "Investigating issue"

# Generate report
./agent report --format slack
```

### Web Dashboard
Open http://localhost:8080 after starting the system

## 🚨 Emergency Stop

```bash
# Stop everything immediately
./agent emergency-stop

# Or manually:
pkill -f "python main.py"
```

## 📈 Success Metrics

### Week 1 Goals
- [ ] 5 PRs successfully merged to staging
- [ ] 0 production incidents
- [ ] <5% error rate

### Month 1 Goals  
- [ ] 50+ issues resolved
- [ ] 90% success rate
- [ ] 2x velocity improvement

## 🔗 Key Resources

1. **[Full Implementation Plan](autonomous-pr-system-plan.md)** - Complete system design
2. **[LangGraph Implementation](autonomous-pr-system-langgraph.md)** - LangGraph-specific architecture
3. **[Implementation Roadmap](implementation-roadmap-langgraph.md)** - Step-by-step build guide with LangGraph
4. **[Linear Integration Guide](linear-integration-strategy.md)** - Backlog management details

## 💡 Getting Help

- **Logs**: Check `logs/` directory
- **Metrics**: View dashboard at localhost:8080
- **Errors**: Check Sentry project
- **Support**: Create issue with `agent-help` label

---

**Remember**: This system is designed to be a helpful assistant, not a replacement for human judgment. Start small, monitor closely, and scale gradually! 🤖✨ 