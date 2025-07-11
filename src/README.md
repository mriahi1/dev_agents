# MVP: Autonomous PR System

A minimal viable implementation that automatically creates PRs from Linear tasks.

## What It Does

1. Reads Linear tasks with `auto-pr-safe` label in "Ready" state
2. Handles simple, safe changes:
   - Fix typos
   - Update text/labels/messages
   - Add loading states
3. Creates PR to staging branch
4. Updates Linear task status automatically

## Quick Start

1. **Setup Environment**
   ```bash
   make setup
   ```

2. **Configure API Keys**
   Edit `.env` file:
   ```
   LINEAR_API_KEY=lin_api_your_key_here
   GITHUB_TOKEN=ghp_your_token_here
   LINEAR_TEAM_ID=your-team-id
   
   # Choose which project to work on (keysy3 or immo)
   TARGET_PROJECT=keysy3
   
   # Map each project to its GitHub repo
   KEYSY3_GITHUB_REPO=owner/keysy3-repo
   IMMO_GITHUB_REPO=owner/immo-repo
   ```
   
   See [Multi-Project Setup Guide](../docs/implementation/multi-project-setup.md) for details.

3. **Verify Setup**
   ```bash
   python scripts/verify_setup.py
   ```

4. **Create Test Task in Linear**
   - Title: "Fix typo in README"
   - Label: `auto-pr-safe`
   - State: "Ready"

5. **Run in Dry Mode**
   ```bash
   make run-dry
   ```

6. **Run for Real**
   ```bash
   make run
   ```

## Architecture

```
Linear Task → Pattern Matching → GitHub PR → Update Linear
```

- **No AI** - Just pattern matching
- **No Complex State** - Simple dictionaries
- **No LangGraph** - Sequential flow only
- **Safe by Design** - Only handles simple changes

## Files

- `main.py` - Main orchestrator
- `agents/creator.py` - Pattern matching for changes
- `integrations/linear_client.py` - Linear API wrapper
- `integrations/github_client.py` - GitHub API wrapper
- `utils/types.py` - Type definitions

## Safety Features

- Only processes tasks with `auto-pr-safe` label
- Rejects complex tasks (long descriptions)
- Creates PRs to staging only
- Dry-run mode by default
- Error handling with Linear updates

## Next Steps

After MVP success, add:
- LangGraph orchestration
- GPT-4 understanding
- Multi-file changes
- Cognitive loops

But first: **Ship this and prove it works!** 