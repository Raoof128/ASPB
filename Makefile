.PHONY: install test lint format clean run help

help:
	@echo "Available commands:"
	@echo "  install    Install dependencies (including dev)"
	@echo "  test       Run tests with coverage"
	@echo "  lint       Run linting checks (black, isort, mypy, flake8)"
	@echo "  format     Format code (black, isort)"
	@echo "  clean      Remove build artifacts and cache"
	@echo "  run        Run the bot (scan)"

install:
	pip install -e .[dev]

test:
	pytest

lint:
	black --check .
	isort --check-only .
	flake8 sp_secret_bot tests
	mypy sp_secret_bot

format:
	black .
	isort .

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	find . -name '__pycache__' -exec rm -rf {} +
	find . -name '*.pyc' -exec rm -rf {} +
	rm -f .coverage

run:
	python3 -m sp_secret_bot.main scan
