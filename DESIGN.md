# System Design and Architecture

This document describes the architectural principles, design decisions, and component boundaries of `shell-anatomy`.

## 1. Architectural Overview

The project is designed with a clean separation of concerns across three core pillars:

```
+-------------------------------------------------------------+
|                      Presentation                           |
|       (Manim Scenes: TerminalHierarchyScene)                |
+------------------------------+------------------------------+
                               |
            +------------------+------------------+
            |                                     |
            v                                     v
+-----------------------+             +-----------------------+
|     Configuration     |             |    Voiceover Layer    |
|   (Tokens & Theme)    |             | (get_speech_service)  |
| - BACKGROUND_COLOR    |             | - ElevenLabsService   |
| - TERMINAL_COLOR      |             | - GTTSService         |
| - SHELL_COLOR         |             | - SilentService       |
| - TEXT_COLOR / BORDER |             +-----------------------+
+-----------------------+
```

### Presentation Layer
Located in `src/shell_anatomy/scenes/`, this layer defines visual constructs and animation timelines using Manim Community Edition (v0.18+). The primary scene `TerminalHierarchyScene` inherits from `VoiceoverScene`, orchestrating visual elements (terminal window chrome, prompt, process memory representation, environment map table) and synchronizing transitions with audio blocks via `with self.voiceover(...)`.

### Configuration and Design Tokens
Located in `src/shell_anatomy/config.py`, this module isolates aesthetic decisions from animation logic. Colors and layout constants reflect a cohesive dark terminal aesthetic:
* `BACKGROUND_COLOR`: Deep slate canvas background (`#0D1117`).
* `TERMINAL_COLOR`: Terminal window accent blue (`#58A6FF`).
* `SHELL_COLOR`: Shell memory green (`#3FB950`).
* `BORDER_COLOR` and `TEXT_COLOR`: Subtle structural borders and high-contrast foreground text.

### Voiceover and Speech Abstraction
Animation timing is driven by speech duration. Rather than hardcoding a single text-to-speech provider, voiceover generation is decoupled into a pluggable service layer.

---

## 2. Voiceover Abstraction

The factory function `get_speech_service()` in `src/shell_anatomy/scenes/terminal_stack.py` inspects the environment to instantiate the appropriate `SpeechService`:

```
                    VOICEOVER_BACKEND
                           |
       +-------------------+-------------------+
       |                   |                   |
"elevenlabs"            "gtts"              "none"
(or default with key)      |                   |
       |             GTTSService        SilentService
ElevenLabsService                       (zero network,
(model: multilingual v2,                word-count timing)
 voice: Brian)
```

### Backends
1. **ElevenLabs (`ElevenLabsService`)**:
   * Production quality speech synthesis.
   * Uses `eleven_multilingual_v2` model with the deep and resonant `Brian` voice (`nPczCjzI2devNBz1zQrb`).
   * Requires `ELEVEN_API_KEY` with `text_to_speech` and `voices_read` permissions.
   * If `ELEVEN_API_KEY` is missing, gracefully falls back to `SilentService`.

2. **Google Text-to-Speech (`GTTSService`)**:
   * Free, cloud-backed alternative using `gTTS`.
   * Ideal for quick local iterations without requiring paid API tokens.

3. **Silent Service (`SilentService`)**:
   * Custom offline `SpeechService` subclass.
   * Generates PCM `.wav` silence files with duration calculated from word count (`max(1.0, words / 2.5)`).
   * Guarantees deterministic, instant scene execution during CI runs and local test development without network dependencies.

---

## 3. Tooling and Packaging Decisions

### Departure from Legacy Templates
Traditional Python templates often rely on heavier or fragmented tooling combinations such as `pip-tools`, `poetry`, or legacy virtualenv management. `shell-anatomy` standardizes on modern Python packaging:

* **Packaging Standard (`pyproject.toml`)**: Follows PEP 517 / PEP 621 using the lightweight, standard-compliant `hatchling` build backend.
* **Modern Package Management (`uv`)**: Utilizes Astral's `uv` for lightning-fast resolution, virtual environment creation, and dependency synchronization.
* **Deterministic Lockfile (`uv.lock`)**: Guarantees identical dependencies across developer workstations and automated workflows.
* **Code Quality**: Uses `ruff` for linting and formatting, combined with `pytest` for automated regression testing.
