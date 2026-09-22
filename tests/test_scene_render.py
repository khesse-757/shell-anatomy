"""Basic import, scene instantiation, and speech service configuration tests."""

from manim_voiceover import VoiceoverScene
from manim_voiceover.services.gtts import GTTSService

from shell_anatomy.config import BACKGROUND_COLOR, SHELL_COLOR
from shell_anatomy.scenes.terminal_stack import (
    SilentService,
    TerminalHierarchyScene,
    get_speech_service,
)


def test_theme_configuration():
    assert BACKGROUND_COLOR.startswith("#")
    assert SHELL_COLOR.startswith("#")


def test_scene_instantiation_silent_mode(monkeypatch):
    monkeypatch.delenv("ELEVEN_API_KEY", raising=False)
    monkeypatch.setenv("VOICEOVER_BACKEND", "none")
    scene = TerminalHierarchyScene()
    assert scene is not None
    assert isinstance(scene, VoiceoverScene)


def test_speech_service_factory_silent_mode(monkeypatch):
    monkeypatch.setenv("VOICEOVER_BACKEND", "none")
    service = get_speech_service()
    assert isinstance(service, SilentService)


def test_speech_service_factory_default_without_api_key(monkeypatch):
    monkeypatch.delenv("ELEVEN_API_KEY", raising=False)
    monkeypatch.delenv("VOICEOVER_BACKEND", raising=False)
    service = get_speech_service()
    assert isinstance(service, SilentService)


def test_speech_service_factory_gtts(monkeypatch):
    monkeypatch.setenv("VOICEOVER_BACKEND", "gtts")
    service = get_speech_service()
    assert isinstance(service, GTTSService)


def test_silent_service_generates_audio(tmp_path):
    service = SilentService(cache_dir=tmp_path)
    result = service.generate_from_text("This is a test sentence for silent audio.")
    assert "original_audio" in result
    audio_file = tmp_path / result["original_audio"]
    assert audio_file.exists()
    assert audio_file.stat().st_size > 0
