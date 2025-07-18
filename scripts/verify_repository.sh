#!/bin/bash

# Repository Verification Script
# Prevents repository confusion by forcing verification before critical operations

set -e

echo "🔍 MANDATORY Repository Verification"
echo "=================================="

# Get current directory
CURRENT_DIR=$(pwd)
BASENAME=$(basename "$CURRENT_DIR")

echo "📍 Current Directory: $CURRENT_DIR"

# Detect project type
if [ -f "package.json" ]; then
    PROJECT_TYPE="React/Node.js"
    echo "📦 Project Type: $PROJECT_TYPE (detected package.json)"
elif [ -f "requirements.txt" ]; then
    PROJECT_TYPE="Python"
    echo "🐍 Project Type: $PROJECT_TYPE (detected requirements.txt)"
else
    PROJECT_TYPE="Unknown"
    echo "❓ Project Type: $PROJECT_TYPE (no package.json or requirements.txt found)"
fi

echo ""

# Task type verification
echo "🎯 Task Type Verification:"
echo "What type of work are you doing?"
echo "1) React/Frontend components (.tsx/.ts files)"
echo "2) Python/DevOps toolkit (.py files)"
echo "3) Documentation (.md files)"
echo "4) Other"

read -p "Enter your choice (1-4): " TASK_TYPE

case $TASK_TYPE in
    1)
        EXPECTED_PROJECT="React/Node.js"
        EXPECTED_DIR="projects/keysy3"
        FILE_TYPES=".tsx/.ts React components"
        ;;
    2)
        EXPECTED_PROJECT="Python"
        EXPECTED_DIR="dev_agents"
        FILE_TYPES=".py Python files"
        ;;
    3)
        EXPECTED_PROJECT="Either"
        EXPECTED_DIR="Either repository"
        FILE_TYPES=".md documentation files"
        ;;
    4)
        echo "⚠️  Manual verification required for other file types"
        exit 0
        ;;
    *)
        echo "❌ Invalid choice. Exiting."
        exit 1
        ;;
esac

echo ""
echo "📋 Verification Results:"
echo "Current Project Type: $PROJECT_TYPE"
echo "Task Requires: $EXPECTED_PROJECT"
echo "File Types: $FILE_TYPES"

# Check for mismatch
if [ "$TASK_TYPE" = "1" ] && [ "$PROJECT_TYPE" != "React/Node.js" ]; then
    echo ""
    echo "❌ CRITICAL ERROR: Repository Mismatch!"
    echo "You're trying to create React components in a $PROJECT_TYPE project."
    echo ""
    echo "🔧 Required Action:"
    echo "Navigate to: $EXPECTED_DIR"
    echo "Command: cd $EXPECTED_DIR"
    echo ""
    echo "Then re-run this verification script."
    exit 1
elif [ "$TASK_TYPE" = "2" ] && [ "$PROJECT_TYPE" != "Python" ]; then
    echo ""
    echo "❌ CRITICAL ERROR: Repository Mismatch!"
    echo "You're trying to create Python files in a $PROJECT_TYPE project."
    echo ""
    echo "🔧 Required Action:"
    echo "Navigate to: $EXPECTED_DIR"
    echo "Command: cd $EXPECTED_DIR"
    echo ""
    echo "Then re-run this verification script."
    exit 1
fi

echo ""
echo "✅ Repository verification passed!"
echo "You are in the correct repository for your task."
echo ""

# Additional safety check for React tasks
if [ "$TASK_TYPE" = "1" ]; then
    if [[ ! "$CURRENT_DIR" == *"keysy3"* ]]; then
        echo "⚠️  WARNING: React task but not in keysy3 directory"
        echo "Current: $CURRENT_DIR"
        echo "Expected: Should contain 'keysy3'"
        echo ""
        read -p "Continue anyway? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            echo "❌ Verification cancelled. Navigate to keysy3 project first."
            exit 1
        fi
    fi
fi

echo "🚀 Proceed with your task!"
echo "Repository: $BASENAME ($PROJECT_TYPE)"
echo "Task: $FILE_TYPES" 