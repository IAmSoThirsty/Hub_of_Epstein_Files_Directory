.PHONY: help setup install clean test docker-build docker-up docker-down fetch-data generate-index

# Default target
.DEFAULT_GOAL := help

# Colors for output
BLUE := \033[0;34m
GREEN := \033[0;32m
YELLOW := \033[1;33m
NC := \033[0m # No Color

help: ## Show this help message
	@echo "$(BLUE)Epstein Files Hub - Available Commands$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  $(GREEN)%-25s$(NC) %s\n", $$1, $$2}'
	@echo ""

# ============================================
# Setup and Installation
# ============================================

setup: ## Run initial setup (creates venv and installs dependencies)
	@echo "$(BLUE)Running setup...$(NC)"
	@chmod +x setup.sh
	@./setup.sh

install: ## Install dependencies in existing environment
	@echo "$(BLUE)Installing dependencies...$(NC)"
	@pip install -r requirements.txt

install-dev: ## Install development dependencies
	@echo "$(BLUE)Installing development dependencies...$(NC)"
	@pip install -r requirements.txt
	@pip install pytest pytest-cov ipython black flake8 mypy

verify: ## Verify installation and dependencies
	@echo "$(BLUE)Verifying setup...$(NC)"
	@python verify-setup.py

# ============================================
# Data Processing
# ============================================

fetch-public-files: ## Fetch FBI Vault and public files
	@echo "$(BLUE)Fetching public files...$(NC)"
	@python scripts/fetch-public-files.py

fetch-wikipedia: ## Fetch Wikipedia data
	@echo "$(BLUE)Fetching Wikipedia data...$(NC)"
	@python scripts/fetch-wikipedia-data.py

process-pdfs: ## Process PDFs with OCR
	@echo "$(BLUE)Processing PDFs...$(NC)"
	@python scripts/process-pdfs.py

generate-index: ## Generate search index
	@echo "$(BLUE)Generating search index...$(NC)"
	@python scripts/generate-search-index.py

safe-source-expand: ## Run safe source discovery
	@echo "$(BLUE)Running safe source expansion...$(NC)"
	@python scripts/safe-source-expander.py

fetch-all: fetch-public-files fetch-wikipedia process-pdfs generate-index ## Fetch and process all data

# ============================================
# Docker Commands
# ============================================

docker-build: ## Build Docker images
	@echo "$(BLUE)Building Docker images...$(NC)"
	@docker-compose build

docker-up: ## Start Docker containers
	@echo "$(BLUE)Starting Docker containers...$(NC)"
	@docker-compose up -d app

docker-down: ## Stop Docker containers
	@echo "$(BLUE)Stopping Docker containers...$(NC)"
	@docker-compose down

docker-logs: ## Show Docker logs
	@docker-compose logs -f app

docker-shell: ## Open shell in Docker container
	@docker-compose exec app /bin/bash

docker-clean: ## Remove all Docker containers, images, and volumes
	@echo "$(YELLOW)Cleaning Docker resources...$(NC)"
	@docker-compose down -v
	@docker system prune -f

docker-fetch-files: ## Fetch public files using Docker
	@echo "$(BLUE)Fetching files with Docker...$(NC)"
	@docker-compose run --rm fetch-public-files

docker-generate-index: ## Generate search index using Docker
	@echo "$(BLUE)Generating index with Docker...$(NC)"
	@docker-compose run --rm generate-search-index

# ============================================
# Development
# ============================================

serve: ## Start local web server
	@echo "$(BLUE)Starting web server at http://localhost:8080$(NC)"
	@cd web && python -m http.server 8080

serve-docker: ## Start web server using Docker
	@echo "$(BLUE)Starting web server with Docker at http://localhost:8080$(NC)"
	@docker-compose --profile web up web

format: ## Format Python code with black
	@echo "$(BLUE)Formatting code...$(NC)"
	@black scripts/ bots/

lint: ## Lint Python code with flake8
	@echo "$(BLUE)Linting code...$(NC)"
	@flake8 scripts/ bots/ --max-line-length=120

type-check: ## Run type checking with mypy
	@echo "$(BLUE)Type checking...$(NC)"
	@mypy scripts/ bots/ --ignore-missing-imports

check: format lint type-check ## Run all code quality checks

# ============================================
# Testing
# ============================================

test: ## Run tests
	@echo "$(BLUE)Running tests...$(NC)"
	@pytest tests/ -v

test-cov: ## Run tests with coverage
	@echo "$(BLUE)Running tests with coverage...$(NC)"
	@pytest tests/ -v --cov=scripts --cov=bots --cov-report=html --cov-report=term

# ============================================
# Cleanup
# ============================================

clean: ## Clean temporary files and cache
	@echo "$(BLUE)Cleaning temporary files...$(NC)"
	@find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	@find . -type f -name "*.pyc" -delete
	@find . -type f -name "*.pyo" -delete
	@find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	@rm -rf .pytest_cache
	@rm -rf htmlcov
	@rm -rf .mypy_cache
	@rm -rf dist build
	@rm -rf tmp/*
	@rm -rf cache/*
	@echo "$(GREEN)Cleanup complete!$(NC)"

clean-data: ## Clean processed data (WARNING: destructive, use FORCE=1 to skip prompt)
	@echo "$(YELLOW)⚠️  WARNING: This will delete all processed data!$(NC)"
	@if [ "$(FORCE)" = "1" ]; then \
		rm -rf data/processed/*; \
		rm -rf data/wikipedia/*; \
		echo "$(GREEN)Data cleaned!$(NC)"; \
	else \
		read -p "Are you sure? [y/N] " -n 1 -r; \
		echo; \
		if [[ $$REPLY =~ ^[Yy]$$ ]]; then \
			rm -rf data/processed/*; \
			rm -rf data/wikipedia/*; \
			echo "$(GREEN)Data cleaned!$(NC)"; \
		else \
			echo "$(BLUE)Cancelled.$(NC)"; \
		fi; \
	fi

clean-all: clean clean-data docker-clean ## Clean everything (WARNING: destructive)

# ============================================
# Deployment
# ============================================

deploy-check: ## Check deployment readiness
	@echo "$(BLUE)Checking deployment readiness...$(NC)"
	@python verify-setup.py
	@echo "$(GREEN)✓ All checks passed!$(NC)"

# ============================================
# Information
# ============================================

info: ## Show project information
	@echo "$(BLUE)Epstein Files Hub$(NC)"
	@echo "Version: 1.0.0"
	@echo ""
	@echo "Python version: $$(python3 --version)"
	@echo "pip version: $$(pip3 --version | cut -d' ' -f2)"
	@echo ""
	@echo "Project directory: $$(pwd)"
	@echo "Virtual environment: $$(if [ -d .venv ]; then echo 'Active (.venv)'; else echo 'Not found'; fi)"
	@echo ""
	@echo "Data directories:"
	@echo "  - data/public_files: $$(du -sh data/public_files 2>/dev/null | cut -f1 || echo 'Empty')"
	@echo "  - data/processed: $$(du -sh data/processed 2>/dev/null | cut -f1 || echo 'Empty')"
	@echo "  - data/wikipedia: $$(du -sh data/wikipedia 2>/dev/null | cut -f1 || echo 'Empty')"
	@echo ""

status: ## Show system status
	@echo "$(BLUE)System Status$(NC)"
	@echo ""
	@echo "Docker status:"
	@docker-compose ps 2>/dev/null || echo "  Docker not running"
	@echo ""
	@echo "Recent logs:"
	@ls -lht logs/ 2>/dev/null | head -5 || echo "  No logs found"

# ============================================
# System Audit and Inspection
# ============================================

system-audit: ## Run comprehensive system-wide audit
	@echo "$(BLUE)Running system-wide audit...$(NC)"
	@python scripts/system-audit.py --format markdown
	@echo "$(GREEN)✓ Audit complete! Check logs/ directory for reports.$(NC)"

system-audit-all: ## Run system audit with all report formats
	@echo "$(BLUE)Running system-wide audit (all formats)...$(NC)"
	@python scripts/system-audit.py --format all
	@echo "$(GREEN)✓ Audit complete! Reports saved in logs/ directory.$(NC)"

system-audit-json: ## Run system audit with JSON output
	@echo "$(BLUE)Running system-wide audit (JSON)...$(NC)"
	@python scripts/system-audit.py --format json
	@echo "$(GREEN)✓ Audit complete! Check logs/ directory for JSON report.$(NC)"

system-audit-quiet: ## Run system audit without console output
	@echo "$(BLUE)Running system-wide audit (quiet mode)...$(NC)"
	@python scripts/system-audit.py --format all --quiet
	@echo "$(GREEN)✓ Audit complete! Reports saved in logs/ directory.$(NC)"

audit-report: ## Alias for system-audit-all
	@$(MAKE) system-audit-all

military-audit: ## Military-style comprehensive system inspection (alias)
	@$(MAKE) system-audit-all
