.PHONY: help install test lint format docs render-silent render-eleven clean

help:
	@echo "Available commands:"
	@echo "  make install       - Install package with dev and docs dependencies"
	@echo "  make test          - Run all tests"
	@echo "  make lint          - Check code quality with ruff"
	@echo "  make format        - Format code with ruff"
	@echo "  make docs          - Build Sphinx documentation"
	@echo "  make render-silent - Render silent preview video (no API key needed)"
	@echo "  make render-eleven - Render high-definition video with ElevenLabs"
	@echo "  make clean         - Remove build artifacts and caches"

install:
	uv pip install -e ".[dev,docs]"

test:
	VOICEOVER_BACKEND=none uv run pytest -v

lint:
	uv run ruff check .
	uv run ruff format --check .

format:
	uv run ruff check --fix .
	uv run ruff format .

docs:
	uv run sphinx-build -b html docs docs/_build/html

render-silent:
	VOICEOVER_BACKEND=none uv run manim -pql src/shell_anatomy/scenes/terminal_stack.py TerminalHierarchyScene

render-eleven:
	VOICEOVER_BACKEND=elevenlabs uv run manim -pqh src/shell_anatomy/scenes/terminal_stack.py TerminalHierarchyScene

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf docs/_build
	find . -type d -name __pycache__ -exec rm -rf {} +
