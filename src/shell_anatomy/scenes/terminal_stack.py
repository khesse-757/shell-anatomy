"""Scene recreating the Terminal vs Shell vs Kernel hierarchy."""

from manim import (
    DOWN,
    ORIGIN,
    UP,
    Arrow,
    FadeIn,
    GrowArrow,
    Rectangle,
    Scene,
    Text,
    VGroup,
    config,
)
from shell_anatomy.config import (
    BACKGROUND_COLOR,
    KERNEL_COLOR,
    SHELL_COLOR,
    TERMINAL_COLOR,
    TEXT_COLOR,
)

config.background_color = BACKGROUND_COLOR


class TerminalHierarchyScene(Scene):
    def construct(self):
        title = Text("The Execution Stack", font="Monospace", font_size=32, color=TEXT_COLOR)
        title.to_edge(UP, buff=0.8)
        self.play(FadeIn(title))

        term_box = Rectangle(width=6.0, height=1.1, color=TERMINAL_COLOR)
        shell_box = Rectangle(width=6.0, height=1.1, color=SHELL_COLOR)
        kernel_box = Rectangle(width=6.0, height=1.1, color=KERNEL_COLOR)

        term_label = Text("Terminal Emulator (GUI / Fonts / Window)", font="Monospace", font_size=16, color=TEXT_COLOR)
        shell_label = Text("Shell (Parser / Environment / Process Control)", font="Monospace", font_size=16, color=TEXT_COLOR)
        kernel_label = Text("Kernel (Hardware / File Systems / CPU Scheduler)", font="Monospace", font_size=16, color=TEXT_COLOR)

        term_group = VGroup(term_box, term_label)
        shell_group = VGroup(shell_box, shell_label)
        kernel_group = VGroup(kernel_box, kernel_label)

        stack = VGroup(term_group, shell_group, kernel_group)
        stack.arrange(DOWN, buff=1.0)
        stack.move_to(ORIGIN + DOWN * 0.4)

        arrow_down_1 = Arrow(term_box.get_bottom(), shell_box.get_top(), buff=0.1, color=TEXT_COLOR)
        arrow_down_2 = Arrow(shell_box.get_bottom(), kernel_box.get_top(), buff=0.1, color=TEXT_COLOR)

        arrow_label_1 = Text("Raw text input", font="Monospace", font_size=13, color=TERMINAL_COLOR)
        arrow_label_1.next_to(arrow_down_1, RIGHT, buff=0.2)

        arrow_label_2 = Text("System calls", font="Monospace", font_size=13, color=SHELL_COLOR)
        arrow_label_2.next_to(arrow_down_2, RIGHT, buff=0.2)

        self.play(FadeIn(term_group))
        self.wait(0.5)

        self.play(GrowArrow(arrow_down_1), FadeIn(arrow_label_1))
        self.play(FadeIn(shell_group))
        self.wait(0.5)

        self.play(GrowArrow(arrow_down_2), FadeIn(arrow_label_2))
        self.play(FadeIn(kernel_group))
        self.wait(2.0)
