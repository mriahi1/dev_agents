# Cursor DevOps Toolkit Makefile

.PHONY: install verify test run-dry run clean lint format type-check help verify-repo

# Installation
install:
	pip install -e .

# Repository verification (CRITICAL SAFETY)
verify-repo:
	@echo "🔍 Running mandatory repository verification..."
	@bash scripts/verify_repository.sh

# Verification and validation
verify: verify-repo
	python scripts/verify_setup.py

# Testing
test: verify-repo
	pytest tests/ -v

# Development
run-dry: verify-repo
	@echo "🧪 Running in dry-run mode..."
	python -m src.main --dry-run

run: verify-repo
	@echo "🚀 Running toolkit..."
	python -m src.main

# Code quality
lint:
	flake8 src/ tests/
	black --check src/ tests/

format:
	black src/ tests/

type-check:
	mypy src/

# Cleanup
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache/
	rm -rf *.egg-info/

# Help
help:
	@echo "🛠️  Cursor DevOps Toolkit"
	@echo ""
	@echo "📍 CRITICAL SAFETY:"
	@echo "  verify-repo    Run repository verification (MANDATORY before any work)"
	@echo ""
	@echo "🚀 Core Commands:"
	@echo "  install        Install the toolkit in development mode"
	@echo "  verify         Run all verification checks"
	@echo "  test           Run the test suite"
	@echo "  run-dry        Run in dry-run mode (safe testing)"
	@echo "  run            Run the toolkit"
	@echo ""
	@echo "🔧 Development:"
	@echo "  lint           Run code linting"
	@echo "  format         Auto-format code"
	@echo "  type-check     Run type checking"
	@echo "  clean          Clean up generated files"
	@echo ""
	@echo "⚠️  ALWAYS run 'make verify-repo' before any coding work!" 