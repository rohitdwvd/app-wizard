# Makefile
.PHONY: install test lint clean build run docker-build docker-run

# Install dependencies
install:
	pip install -r requirements.txt
	pip install -e .

# Install development dependencies
install-dev:
	pip install -r requirements.txt
	pip install -e .
	pip install pytest pytest-cov black isort flake8 mypy

# Run tests
test:
	python -m pytest tests/ -v

# Run tests with coverage
test-coverage:
	python -m pytest tests/ -v --cov=src --cov-report=html

# Lint code
lint:
	black src/ tests/
	isort src/ tests/
	flake8 src/ tests/
	mypy src/

# Clean build artifacts
clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	find . -type d -name __pycache__ -delete
	find . -type f -name "*.pyc" -delete

# Build package
build: clean
	python setup.py sdist bdist_wheel

# Run the server
run:
	python -m src.main

# Run examples
examples:
	python examples/run_examples.py

# Docker build
docker-build:
	docker build -t address-mcp-server .

# Docker run with Ollama
docker-run:
	docker-compose up

# Install Ollama and setup models
setup-ollama:
	@echo "Installing Ollama models..."
	ollama pull llama3.2:1b
	ollama pull llama3.2:3b
	@echo "✅ Ollama models installed"

# Check system requirements
check-system:
	@echo "🔍 Checking system requirements..."
	@python --version
	@pip --version
	@echo "✅ Python environment ready"
