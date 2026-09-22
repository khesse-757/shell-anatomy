"""Basic import and configuration tests."""

from shell_anatomy.config import BACKGROUND_COLOR, SHELL_COLOR
from shell_anatomy.scenes.terminal_stack import TerminalHierarchyScene


def test_theme_configuration():
    assert BACKGROUND_COLOR.startswith("#")
    assert SHELL_COLOR.startswith("#")


def test_scene_instantiation():
    scene = TerminalHierarchyScene()
    assert scene is not None
