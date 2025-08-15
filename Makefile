# VOITHER Documentation Makefile
# Simple commands for maintaining documentation

.PHONY: help validate validate-quick links spell-check clean serve

# Default target
help:
	@echo "VOITHER Documentation Maintenance"
	@echo "================================="
	@echo ""
	@echo "Available commands:"
	@echo "  validate       - Full validation (links + files)"
	@echo "  validate-quick - Quick validation (files only)"
	@echo "  links          - Check internal links only"
	@echo "  spell-check    - Run spell checker (if available)"
	@echo "  stats          - Show documentation statistics"
	@echo "  clean          - Clean temporary files"
	@echo "  serve          - Serve docs locally (if server available)"
	@echo ""
	@echo "Examples:"
	@echo "  make validate      # Full check"
	@echo "  make links         # Check links only"
	@echo "  make stats         # Show statistics"

# Validation commands
validate:
	@echo "🔍 Running full documentation validation..."
	python3 scripts/validate-docs.py .

validate-quick:
	@echo "⚡ Running quick validation..."
	python3 scripts/validate-docs.py --quick .

links:
	@echo "🔗 Checking internal links..."
	python3 scripts/validate-docs.py .

# Statistics
stats:
	@echo "📊 VOITHER Documentation Statistics"
	@echo "=================================="
	@echo "Markdown files: $$(find . -name '*.md' -not -path './.git/*' | wc -l)"
	@echo "Total lines: $$(find . -name '*.md' -not -path './.git/*' -exec cat {} \; | wc -l)"
	@echo "Python files: $$(find . -name '*.py' -not -path './.git/*' | wc -l)"
	@echo "Image files: $$(find . -name '*.png' -o -name '*.jpg' -o -name '*.gif' | wc -l)"
	@echo "Video files: $$(find . -name '*.mp4' -o -name '*.mov' | wc -l)"
	@echo ""
	@echo "Largest files:"
	@find . -name '*.md' -not -path './.git/*' -exec wc -l {} \; | sort -nr | head -5

# Spell checking (if available)
spell-check:
	@echo "🔤 Running spell check..."
	@if command -v cspell >/dev/null 2>&1; then \
		cspell "**/*.md"; \
	elif command -v aspell >/dev/null 2>&1; then \
		find . -name '*.md' -not -path './.git/*' -exec aspell check {} \;; \
	else \
		echo "❌ No spell checker found. Install cspell or aspell."; \
		echo "   npm install -g cspell"; \
		echo "   # or"; \
		echo "   sudo apt-get install aspell"; \
	fi

# Clean temporary files
clean:
	@echo "🧹 Cleaning temporary files..."
	find . -name '*.tmp' -delete
	find . -name '*.bak' -delete
	find . -name '*~' -delete
	find . -name '.DS_Store' -delete
	@echo "✅ Cleanup complete"

# Local server (if available)
serve:
	@echo "🌐 Starting local documentation server..."
	@if command -v python3 >/dev/null 2>&1; then \
		echo "📡 Server running at http://localhost:8000"; \
		echo "Press Ctrl+C to stop"; \
		python3 -m http.server 8000; \
	elif command -v python >/dev/null 2>&1; then \
		echo "📡 Server running at http://localhost:8000"; \
		echo "Press Ctrl+C to stop"; \
		python -m SimpleHTTPServer 8000; \
	else \
		echo "❌ Python not found. Cannot start server."; \
	fi

# Development helpers
dev-setup:
	@echo "🛠️  Setting up development environment..."
	@if command -v npm >/dev/null 2>&1; then \
		echo "Installing Node.js tools..."; \
		npm install -g cspell markdown-link-check; \
	else \
		echo "⚠️  npm not found. Skipping Node.js tools."; \
	fi
	@echo "✅ Development setup complete"

# Git hooks
install-hooks:
	@echo "🪝 Installing Git hooks..."
	@if [ -d .git ]; then \
		echo "#!/bin/bash" > .git/hooks/pre-commit; \
		echo "make validate-quick" >> .git/hooks/pre-commit; \
		chmod +x .git/hooks/pre-commit; \
		echo "✅ Pre-commit hook installed"; \
	else \
		echo "❌ Not a Git repository"; \
	fi

# Search functionality
search:
	@if [ -z "$(TERM)" ]; then \
		echo "❌ Usage: make search TERM='your search term'"; \
	else \
		echo "🔍 Searching for '$(TERM)' in documentation..."; \
		grep -r -n --include="*.md" "$(TERM)" . || echo "No results found"; \
	fi

# Word count for specific file
word-count:
	@if [ -z "$(FILE)" ]; then \
		echo "❌ Usage: make word-count FILE='filename.md'"; \
	else \
		wc -w "$(FILE)"; \
	fi

# Test backup workflow
test-backup:
	@echo "🧪 Testing backup workflow components..."
	python3 scripts/test-backup-workflow.py

# Validate workflow files
validate-workflows:
	@echo "🔍 Validating GitHub Actions workflows..."
	@for workflow in .github/workflows/*.yml; do \
		echo "Validating $$workflow..."; \
		python3 -c "import yaml; yaml.safe_load(open('$$workflow'))" && echo "✅ $$workflow valid" || echo "❌ $$workflow invalid"; \
	done