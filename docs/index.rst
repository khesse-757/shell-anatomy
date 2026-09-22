shell-anatomy documentation
===========================

Visual explanations of shell internals, process lifecycles, and environment resolution built with Manim Community Edition and automated voiceovers.

.. toctree::
   :maxdepth: 2
   :caption: Contents:

Architecture and Design
-----------------------

The system architecture separates visual rendering from configuration and speech services:

* **Presentation**: Manim scenes defining vector animation timelines.
* **Configuration**: Color palettes, tokens, and aesthetic styling.
* **Voiceover Services**: Pluggable speech synthesis backends (ElevenLabs, gTTS, SilentService).

Usage and Rendering
-------------------

.. code-block:: bash

   # Fast silent preview for testing and CI
   VOICEOVER_BACKEND=none manim -pql src/shell_anatomy/scenes/terminal_stack.py TerminalHierarchyScene

   # High-definition production render with ElevenLabs narration
   VOICEOVER_BACKEND=elevenlabs manim -pqh src/shell_anatomy/scenes/terminal_stack.py TerminalHierarchyScene

   # Free scratch render with Google Text-to-Speech
   VOICEOVER_BACKEND=gtts manim -pql src/shell_anatomy/scenes/terminal_stack.py TerminalHierarchyScene

API Reference
-------------

Configuration
~~~~~~~~~~~~~

.. automodule:: shell_anatomy.config
   :members:
   :undoc-members:
   :show-inheritance:

Terminal Stack Scene and Speech Services
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. automodule:: shell_anatomy.scenes.terminal_stack
   :members:
   :undoc-members:
   :show-inheritance:
