"""Sphinx configuration file for shell-anatomy documentation."""

import os
import sys

# Insert src directory to path for autodoc discovery
sys.path.insert(0, os.path.abspath("../src"))

project = "shell-anatomy"
author = "Kyle Hesse"
copyright = "2026, Kyle Hesse"
release = "0.1.0"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_autodoc_typehints",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "furo"
html_static_path = ["_static"]

# Napoleon settings for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_use_param = True
napoleon_use_rtype = True
autodoc_member_order = "bysource"
