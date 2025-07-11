# ✅ Pre-Implementation Verification Checklist

## Before You Start Building

Run through this checklist to ensure smooth implementation.

## 1. Environment Ready

```bash
# Check Python version
python --version  # Should be 3.10+

# Check PostgreSQL
psql --version   # Should be 14+

# Check Redis
redis-cli ping   # Should return PONG
```

## 2. API Keys Configured

```python
# scripts/verify_keys.py
import os
from dotenv import load_dotenv

load_dotenv()

checks = {
    "LINEAR_API_KEY": os.getenv("LINEAR_API_KEY", "").startswith("lin_api_"),
    "GITHUB_TOKEN": os.getenv("GITHUB_TOKEN", "").startswith("ghp_"),
    "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY", "").startswith("sk-"),
    "LINEAR_TEAM_ID": len(os.getenv("LINEAR_TEAM_ID", "")) > 0,
    "GITHUB_REPO": "/" in os.getenv("GITHUB_REPO", ""),
}

for key, valid in checks.items():
    print(f"{'✅' if valid else '❌'} {key}")
```

## 3. Linear Setup Verified

- [ ] Team ID is correct
- [ ] "auto-pr-safe" label exists
- [ ] Workflow states configured:
  - [ ] "Ready" state exists
  - [ ] "In Progress" state exists  
  - [ ] "In Review" state exists
  - [ ] "Done" state exists
- [ ] Test issue created with:
  - Title: "Fix typo in README"
  - Label: "auto-pr-safe"
  - State: "Ready"

## 4. GitHub Repository Ready

- [ ] Repository has `staging` branch
- [ ] Branch protection rules:
  - [ ] `main` protected from direct push
  - [ ] `staging` allows PR merges
- [ ] Bot has permissions:
  - [ ] Read repository
  - [ ] Write issues
  - [ ] Write pull requests
  - [ ] Write contents

## 5. Safety Measures in Place

- [ ] `.env` file NOT committed
- [ ] `DRY_RUN_MODE=true` in .env
- [ ] `MAX_PR_COMPLEXITY=3` set
- [ ] Backup of important repos

## 6. Code Quality Tools

```bash
# Install and verify
pip install mypy black flake8 pytest

# Run checks
mypy --version
black --version  
flake8 --version
pytest --version
```

## 7. Test Data Prepared

Create these test Linear issues:

1. **Simple Typo Fix**
   ```
   Title: Fix typo in README
   Description: Change "recieve" to "receive" 
   Label: auto-pr-safe
   Estimate: 1
   ```

2. **Text Update**
   ```
   Title: Update welcome message
   Description: Change welcome text to "Hello, World!"
   Label: auto-pr-safe
   Estimate: 1
   ```

3. **Unsafe Issue (Should Skip)**
   ```
   Title: Update authentication logic
   Description: Refactor auth system
   Label: auto-pr-safe
   Estimate: 5
   ```

## 8. Project Structure Created

```bash
# Run this to create structure
mkdir -p src/{agents,integrations,utils}
mkdir -p tests/{unit,integration}
mkdir -p scripts
mkdir -p logs

# Create __init__.py files
find src -type d -exec touch {}/__init__.py \;
```

## 9. Dependencies Installed

```bash
# Create minimal requirements.txt first
cat > requirements.txt << EOF
# Core
PyGithub==2.1.1
httpx==0.25.2
python-dotenv==1.0.0
loguru==0.7.2
pydantic==2.5.0
tenacity==8.2.3
pytest==7.4.3
pytest-asyncio==0.21.1
mypy==1.7.1
EOF

# Install
pip install -r requirements.txt
```

## 10. Monitoring Ready

- [ ] Terminal ready for logs
- [ ] Linear page open to watch status
- [ ] GitHub repo page ready
- [ ] Error log location known: `logs/`

## Quick Verification Script

```python
# scripts/pre_flight_check.py
#!/usr/bin/env python3
"""Run all pre-flight checks"""

import os
import sys
import subprocess
from pathlib import Path

def check_command(cmd, name):
    try:
        subprocess.run(cmd, shell=True, check=True, capture_output=True)
        print(f"✅ {name}")
        return True
    except:
        print(f"❌ {name}")
        return False

def check_file(path, name):
    if Path(path).exists():
        print(f"✅ {name}")
        return True
    else:
        print(f"❌ {name}")
        return False

def main():
    print("🚀 Pre-flight Check\n")
    
    checks_passed = 0
    checks_total = 0
    
    # Environment checks
    print("Environment:")
    for cmd, name in [
        ("python --version", "Python installed"),
        ("psql --version", "PostgreSQL installed"),
        ("redis-cli ping", "Redis running"),
    ]:
        if check_command(cmd, name):
            checks_passed += 1
        checks_total += 1
    
    # File checks
    print("\nConfiguration:")
    for path, name in [
        (".env", ".env file exists"),
        ("src/", "src directory exists"),
        ("tests/", "tests directory exists"),
    ]:
        if check_file(path, name):
            checks_passed += 1
        checks_total += 1
    
    # API key checks
    print("\nAPI Keys:")
    from dotenv import load_dotenv
    load_dotenv()
    
    for key in ["LINEAR_API_KEY", "GITHUB_TOKEN", "LINEAR_TEAM_ID", "GITHUB_REPO"]:
        if os.getenv(key):
            print(f"✅ {key} set")
            checks_passed += 1
        else:
            print(f"❌ {key} missing")
        checks_total += 1
    
    # Summary
    print(f"\n{'='*40}")
    print(f"Passed: {checks_passed}/{checks_total}")
    
    if checks_passed == checks_total:
        print("✅ All checks passed! Ready to implement.")
        return 0
    else:
        print("❌ Some checks failed. Please fix before proceeding.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
```

## Ready to Build?

Once all checks pass:

1. Start with the [MVP Implementation](mvp-implementation.md)
2. Follow the implementation order strictly  
3. Test each component before moving on
4. Use dry-run mode for first tests
5. Monitor everything closely

Remember: **Start simple, test everything, safety first!** 