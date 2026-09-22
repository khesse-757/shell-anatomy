# shell-anatomy

Visual explanations of shell internals, process lifecycles, and environment resolution built with Manim Community Edition.

Inspired by Ryan Baker's video "How the Shell Works" and styled after the terminal aesthetic of https://kahdev.me/.

## Quickstart

Prerequisites:
* Python 3.11+
* uv
* ffmpeg

```bash
uv venv
source .venv/bin/activate
uv pip install -e ".[dev]"

# Preview render
manim -pql src/shell_anatomy/scenes/terminal_stack.py TerminalHierarchyScene
```

## Tests
```bash
pytest
```
