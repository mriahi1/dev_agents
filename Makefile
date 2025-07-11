.PHONY: help setup install test clean lint format run cli

# Default target
help:
	@echo "Cursor DevOps Toolkit"
	@echo ""
	@echo "Available commands:"
	@echo "  make setup    - Create virtual environment and install dependencies"
	@echo "  make install  - Install the toolkit as a command"
	@echo "  make test     - Run tests"
	@echo "  make lint     - Run linting"
	@echo "  make format   - Format code"
	@echo "  make clean    - Clean up generated files"
	@echo ""
	@echo "Usage examples:"
	@echo "  python -m src.main linear list"
	@echo "  python -m src.main github pr create --help"

# Setup virtual environment
setup:
	@echo "🔧 Setting up virtual environment..."
	python3 -m venv venv
	./venv/bin/pip install --upgrade pip
	./venv/bin/pip install -r requirements.txt
	@echo "✅ Setup complete!"
	@echo ""
	@echo "Activate with: source venv/bin/activate"

# Install as editable package
install: setup
	@echo "📦 Installing toolkit..."
	./venv/bin/pip install -e .
	@echo "✅ Toolkit installed!"

# Run tests
test:
	@echo "🧪 Running tests..."
	./venv/bin/pytest tests/ -v

# Linting
lint:
	@echo "🔍 Running linting..."
	./venv/bin/mypy src/
	./venv/bin/flake8 src/ tests/

# Format code
format:
	@echo "✨ Formatting code..."
	./venv/bin/black src/ tests/

# Clean up
clean:
	@echo "🧹 Cleaning up..."
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf *.egg-info

# Quick access to CLI
cli:
	@python -m src.main 