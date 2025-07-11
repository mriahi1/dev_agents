#!/usr/bin/env python3
"""Verify MVP setup"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def check_env_vars():
    """Check required environment variables"""
    print("🔍 Checking environment variables...")
    
    # Core required variables
    required = {
        "LINEAR_API_KEY": lambda v: v.startswith("lin_api_"),
        "GITHUB_TOKEN": lambda v: v.startswith("ghp_"),
        "LINEAR_TEAM_ID": lambda v: len(v) > 0,
        "TARGET_PROJECT": lambda v: len(v) > 0
    }
    
    all_good = True
    for key, validator in required.items():
        value = os.getenv(key, "")
        if value and validator(value):
            print(f"✅ {key} is set")
        else:
            print(f"❌ {key} is missing or invalid")
            all_good = False
    
    # Check for project-specific GitHub repo
    target_project = os.getenv("TARGET_PROJECT", "")
    if target_project:
        repo_env_var = f"{target_project.upper().replace('-', '_')}_GITHUB_REPO"
        github_repo = os.getenv(repo_env_var, "")
        if github_repo and "/" in github_repo:
            print(f"✅ {repo_env_var} is set to {github_repo}")
        else:
            print(f"❌ {repo_env_var} is missing or invalid")
            all_good = False
    
    return all_good

def check_imports():
    """Check required packages are installed"""
    print("\n🔍 Checking Python packages...")
    
    packages = [
        "github",
        "httpx", 
        "pydantic",
        "loguru",
        "tenacity",
        "dotenv",
        "pytest"
    ]
    
    all_good = True
    for package in packages:
        try:
            __import__(package)
            print(f"✅ {package} installed")
        except ImportError:
            print(f"❌ {package} missing - run 'pip install -r requirements.txt'")
            all_good = False
    
    return all_good

def check_structure():
    """Check project structure exists"""
    print("\n🔍 Checking project structure...")
    
    paths = [
        "src/",
        "src/agents/",
        "src/integrations/",
        "src/utils/",
        "tests/",
        "scripts/"
    ]
    
    all_good = True
    for path in paths:
        if os.path.exists(path):
            print(f"✅ {path} exists")
        else:
            print(f"❌ {path} missing")
            all_good = False
    
    return all_good

def main():
    print("🚀 MVP Setup Verification\n")
    
    checks = [
        check_structure(),
        check_imports(),
        check_env_vars()
    ]
    
    if all(checks):
        print("\n✅ All checks passed! Ready to run MVP.")
        print("\nNext steps:")
        print("1. Create a test Linear issue with 'auto-pr-safe' label")
        print("2. Run 'make run-dry' to test in dry-run mode")
        print("3. Run 'make run' when ready for production")
        return 0
    else:
        print("\n❌ Some checks failed. Please fix before continuing.")
        return 1

if __name__ == "__main__":
    sys.exit(main()) 