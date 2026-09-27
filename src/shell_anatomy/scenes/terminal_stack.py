"""Terminal stack hierarchy scene and speech service factory.

This module defines the primary Manim visualization illustrating the boundary
between terminal emulators and shell processes, along with speech service abstractions.
"""

import os
import wave
from os import PathLike
from pathlib import Path

from manim import (
    DOWN,
    LEFT,
    RIGHT,
    UP,
    AddTextLetterByLetter,
    Circle,
    FadeIn,
    FadeOut,
    Indicate,
    Line,
    RoundedRectangle,
    SurroundingRectangle,
    Text,
    VGroup,
    config,
)
from manim_voiceover import VoiceoverScene
from manim_voiceover._typing import VoiceoverData
from manim_voiceover.services.base import SpeechService
from manim_voiceover.services.elevenlabs import ElevenLabsService
from manim_voiceover.services.gtts import GTTSService

from shell_anatomy.config import (
    BACKGROUND_COLOR,
    BORDER_COLOR,
    SHELL_COLOR,
    TERMINAL_COLOR,
    TEXT_COLOR,
)

config.background_color = BACKGROUND_COLOR


class SilentService(SpeechService):
    """Fallback speech service that generates silent audio with duration based on word count.

    This service is designed for deterministic local testing and continuous integration
    without requiring third-party API credentials or network access.

    Args:
        words_per_second: Estimated speaking rate used to derive duration from word count.
        **kwargs: Additional keyword arguments forwarded to SpeechService.
    """

    def __init__(self, words_per_second: float = 2.5, **kwargs: object) -> None:
        """Initializes the SilentService with a target speaking rate."""
        self.words_per_second = words_per_second
        super().__init__(transcription_model=None, **kwargs)

    def generate_from_text(
        self,
        text: str,
        cache_dir: PathLike | None = None,
        path: PathLike | None = None,
        **kwargs: object,
    ) -> VoiceoverData:
        """Generates a silent PCM WAV audio file with duration scaled by word count.

        Args:
            text: The text to convert into a timed silent audio segment.
            cache_dir: Optional custom directory to store generated audio.
            path: Optional explicit filename or path for the generated audio file.
            **kwargs: Additional generation options (unused).

        Returns:
            A dictionary containing input text, metadata, and relative audio file path.
        """
        cache_dir_path = (
            Path(cache_dir) if cache_dir is not None else Path(self.cache_dir)
        )
        cache_dir_path.mkdir(parents=True, exist_ok=True)

        input_data = {"input_text": text, "service": "silent"}
        cached_result = self.get_cached_result(input_data, cache_dir_path)
        if cached_result is not None:
            return cached_result

        if path is None:
            audio_path = self.get_audio_basename(input_data) + ".wav"
        else:
            audio_path = str(path)

        full_audio_path = cache_dir_path / audio_path
        if not full_audio_path.exists():
            words = len(text.split())
            duration = max(1.0, words / self.words_per_second)
            with wave.open(str(full_audio_path), "w") as wav_file:
                wav_file.setnchannels(1)
                wav_file.setsampwidth(2)
                wav_file.setframerate(44100)
                num_frames = int(duration * 44100)
                wav_file.writeframes(b"\x00" * (num_frames * 2))

        return {
            "input_text": text,
            "input_data": input_data,
            "original_audio": audio_path,
        }


def get_speech_service() -> SpeechService:
    """Factory function for selecting speech service based on VOICEOVER_BACKEND.

    Inspects the `VOICEOVER_BACKEND` environment variable and returns one of:
    - `ElevenLabsService`: Production neural speech using Brian voice (`elevenlabs`).
    - `GTTSService`: Google Text-to-Speech service (`gtts`).
    - `SilentService`: Offline silence generator with word-count durations (`none` or default).

    Returns:
        An instantiated SpeechService subclass ready for use in VoiceoverScene.
    """
    backend = os.environ.get("VOICEOVER_BACKEND", "").strip().lower()
    has_eleven_key = bool(os.environ.get("ELEVEN_API_KEY"))

    if backend == "gtts":
        return GTTSService(transcription_model=None)
    if backend == "elevenlabs":
        if not has_eleven_key:
            return SilentService()
        return ElevenLabsService(
            voice_name="Brian - Deep, Resonant and Comforting",
            model="eleven_multilingual_v2",
            transcription_model=None,
        )
    if backend == "none":
        return SilentService()

    # Default fallback: use ElevenLabs if ELEVEN_API_KEY is present, otherwise SilentService
    if has_eleven_key:
        return ElevenLabsService(
            voice_name="Brian - Deep, Resonant and Comforting",
            model="eleven_multilingual_v2",
            transcription_model=None,
        )
    return SilentService()


class TerminalHierarchyScene(VoiceoverScene):
    """Manim scene visualizing terminal emulator vs shell process separation and variable lookup."""

    def construct(self) -> None:
        """Constructs and animates the terminal stack hierarchy and variable resolution."""
        self.set_speech_service(get_speech_service())

        term_bg = RoundedRectangle(
            corner_radius=0.15,
            width=10.0,
            height=2.8,
            color=BORDER_COLOR,
            fill_color="#161B22",
            fill_opacity=1.0,
        )
        term_bg.to_edge(UP, buff=0.5)

        btn_r = Circle(radius=0.07, color="#FF5F56", fill_opacity=1.0)
        btn_y = Circle(radius=0.07, color="#FFBD2E", fill_opacity=1.0)
        btn_g = Circle(radius=0.07, color="#27C93F", fill_opacity=1.0)
        btns = VGroup(btn_r, btn_y, btn_g).arrange(RIGHT, buff=0.12)
        btns.move_to(term_bg.get_corner(UP + LEFT) + RIGHT * 0.45 + DOWN * 0.3)

        term_title = Text(
            "Terminal Emulator", font="Monospace", font_size=13, color=TERMINAL_COLOR
        )
        term_title.next_to(btns, RIGHT, buff=0.35)

        title_sep = Line(
            start=term_bg.get_left() + UP * 0.8,
            end=term_bg.get_right() + UP * 0.8,
            color=BORDER_COLOR,
            stroke_width=1.5,
        )
        term_chrome = VGroup(term_bg, btns, term_title, title_sep)

        prompt_pos = term_bg.get_corner(UP + LEFT) + RIGHT * 0.5 + DOWN * 0.95
        prompt_symbol = Text("$ ", font="Monospace", font_size=18, color=SHELL_COLOR)
        prompt_symbol.move_to(prompt_pos, aligned_edge=LEFT)

        cmd_text = Text("echo $SHELL", font="Monospace", font_size=18, color=TEXT_COLOR)
        cmd_text.next_to(prompt_symbol, RIGHT, buff=0.12)

        out_pos = prompt_pos + DOWN * 0.55
        out_text = Text("/bin/zsh", font="Monospace", font_size=18, color=TEXT_COLOR)
        out_text.move_to(out_pos, aligned_edge=LEFT)

        shell_box = RoundedRectangle(
            corner_radius=0.15,
            width=10.0,
            height=3.4,
            color=SHELL_COLOR,
            fill_color="#0D1F17",
            fill_opacity=0.6,
        )
        shell_box.next_to(term_bg, DOWN, buff=0.5)

        shell_header = Text(
            "Shell Process Memory (PID: 41209)",
            font="Monospace",
            font_size=14,
            color=SHELL_COLOR,
        )
        shell_header.move_to(
            shell_box.get_corner(UP + LEFT) + RIGHT * 0.5 + DOWN * 0.35,
            aligned_edge=LEFT,
        )

        env_label = Text(
            "Environment Map", font="Monospace", font_size=12, color=TEXT_COLOR
        )
        env_label.next_to(shell_header, DOWN, buff=0.25, aligned_edge=LEFT)

        r1_k = Text("USER", font="Monospace", font_size=14, color=BORDER_COLOR)
        r1_sep = Text(" -> ", font="Monospace", font_size=14, color=BORDER_COLOR)
        r1_v = Text("kyle", font="Monospace", font_size=14, color=BORDER_COLOR)
        row_user = VGroup(r1_k, r1_sep, r1_v).arrange(RIGHT, buff=0.1)

        r2_k = Text("SHELL", font="Monospace", font_size=15, color=TEXT_COLOR)
        r2_sep = Text(" -> ", font="Monospace", font_size=15, color=TEXT_COLOR)
        r2_v = Text("/bin/zsh", font="Monospace", font_size=15, color=SHELL_COLOR)
        row_shell = VGroup(r2_k, r2_sep, r2_v).arrange(RIGHT, buff=0.1)

        r3_k = Text("PATH", font="Monospace", font_size=14, color=BORDER_COLOR)
        r3_sep = Text(" -> ", font="Monospace", font_size=14, color=BORDER_COLOR)
        r3_v = Text("/usr/bin:/bin", font="Monospace", font_size=14, color=BORDER_COLOR)
        row_path = VGroup(r3_k, r3_sep, r3_v).arrange(RIGHT, buff=0.1)

        env_table = VGroup(row_user, row_shell, row_path).arrange(
            DOWN, aligned_edge=LEFT, buff=0.2
        )
        env_table.next_to(env_label, DOWN, buff=0.2, aligned_edge=LEFT)
        env_surround = SurroundingRectangle(
            env_table, color=BORDER_COLOR, buff=0.18, corner_radius=0.08
        )

        with self.voiceover(
            text="When you type into a terminal window, the terminal emulator simply handles the visuals and accepts raw keystrokes."
        ):
            self.play(FadeIn(term_chrome), run_time=1.0)
            self.play(FadeIn(prompt_symbol), run_time=0.4)
            self.play(AddTextLetterByLetter(cmd_text, run_time=1.6))

        with self.voiceover(
            text="Running inside it is the shell, an active process with its own PID and a private memory space."
        ):
            self.play(FadeIn(shell_box), FadeIn(shell_header), run_time=1.0)
            self.play(
                FadeIn(env_label), FadeIn(env_surround), FadeIn(env_table), run_time=1.0
            )

        with self.voiceover(
            text="Before executing the command, the shell intercepts the dollar sign expansion operator and searches its internal environment map for the key SHELL."
        ):
            query_token = Text(
                "lookup: $SHELL", font="Monospace", font_size=14, color=TERMINAL_COLOR
            )
            query_token.move_to(cmd_text.get_right() + LEFT * 0.4)
            target_query_pos = r2_k.get_left() + LEFT * 1.5
            self.play(query_token.animate.move_to(target_query_pos), run_time=1.2)
            self.play(
                Indicate(r2_k, color=TERMINAL_COLOR, scale_factor=1.12), run_time=0.8
            )

        with self.voiceover(
            text="The resolved value, the path to the Z-shell binary, is extracted and returned to the terminal output."
        ):
            extracted_val = r2_v.copy()
            self.play(
                FadeOut(query_token),
                extracted_val.animate.set_color(TERMINAL_COLOR)
                .scale(1.1)
                .shift(RIGHT * 0.3),
                run_time=0.8,
            )
            self.play(
                extracted_val.animate.move_to(out_text.get_center())
                .set_color(TEXT_COLOR)
                .scale(18 / 16.5),
                run_time=1.2,
            )
            self.remove(extracted_val)
            self.add(out_text)

        self.wait(1.5)
