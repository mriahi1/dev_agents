#!/bin/bash

# Environment Setup Script
# Adds repository verification functions to shell environment

echo "🔧 Setting up repository verification environment..."

# Detect shell
SHELL_NAME=$(basename "$SHELL")
echo "📍 Detected shell: $SHELL_NAME"

# Function to add to shell RC file
setup_shell_functions() {
    local RC_FILE="$1"
    
    cat >> "$RC_FILE" << 'EOF'

# Repository Verification Functions
# Added by dev_agents setup

# Quick repository check
repo_check() {
    echo "🔍 Repository Check"
    echo "📍 Current: $(pwd)"
    echo "📍 Basename: $(basename $(pwd))"
    
    if [ -f package.json ]; then
        echo "📦 Type: React/Node.js (package.json found)"
    elif [ -f requirements.txt ]; then
        echo "🐍 Type: Python (requirements.txt found)"
    else
        echo "❓ Type: Unknown (no package.json or requirements.txt)"
    fi
    
    echo "📋 Files:"
    ls -la | head -10
}

# Quick navigation with verification
goto_keysy3() {
    echo "🚀 Navigating to keysy3..."
    cd /Users/maximeriahi/Projects/dev_agents/projects/keysy3/
    repo_check
}

goto_devagents() {
    echo "🚀 Navigating to dev_agents..."
    cd /Users/maximeriahi/Projects/dev_agents/
    repo_check
}

# Safe file creation with verification
safe_touch() {
    local FILE="$1"
    
    if [[ "$FILE" == *.tsx ]] || [[ "$FILE" == *.ts ]] || [[ "$FILE" == *.jsx ]]; then
        if [ ! -f package.json ]; then
            echo "❌ ERROR: Creating React file outside React project!"
            echo "Current: $(pwd)"
            echo "Required: package.json must exist"
            echo "Fix: Run 'goto_keysy3' first"
            return 1
        fi
    fi
    
    if [[ "$FILE" == *.py ]]; then
        if [ ! -f requirements.txt ]; then
            echo "❌ ERROR: Creating Python file outside Python project!"
            echo "Current: $(pwd)"
            echo "Required: requirements.txt must exist"
            echo "Fix: Run 'goto_devagents' first"
            return 1
        fi
    fi
    
    echo "✅ Creating $FILE in $(basename $(pwd))"
    touch "$FILE"
}

# Aliases for convenience
alias rc='repo_check'
alias gk='goto_keysy3'
alias gd='goto_devagents'
alias st='safe_touch'

EOF

    echo "✅ Added functions to $RC_FILE"
}

# Setup based on shell type
case "$SHELL_NAME" in
    zsh)
        RC_FILE="$HOME/.zshrc"
        setup_shell_functions "$RC_FILE"
        echo "🔄 Reload with: source ~/.zshrc"
        ;;
    bash)
        RC_FILE="$HOME/.bashrc"
        setup_shell_functions "$RC_FILE"
        echo "🔄 Reload with: source ~/.bashrc"
        ;;
    *)
        echo "⚠️  Unsupported shell: $SHELL_NAME"
        echo "Manual setup required"
        ;;
esac

echo ""
echo "🎯 New Commands Available:"
echo "  rc           - Quick repository check"
echo "  gk           - Go to keysy3 project"
echo "  gd           - Go to dev_agents project"  
echo "  st <file>    - Safe touch (with verification)"
echo "  repo_check   - Detailed repository verification"
echo ""
echo "✅ Environment setup complete!"
echo "Restart your terminal or run the source command above." 