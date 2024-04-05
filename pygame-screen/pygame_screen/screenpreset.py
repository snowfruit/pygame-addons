import math
import pygame
from .screenfit import *

# Nothing fancy. Retro is sharp-blocky, modern is blurry-smooth.


class ScreenRetroContain(ScreenContain):
    """Based on ScreenContain-object. With a blocky retro-style."""

    def __init__(self, canvas_size: tuple[int, int]) -> None:
        super().__init__(canvas_size)
        self.use_integer_scaling = True
        self.use_smooth = False


class ScreenRetroCover(ScreenCover):
    """Based on ScreenCover-object. With a blocky retro-style."""

    def __init__(self, canvas_size: tuple[int, int]) -> None:
        super().__init__(canvas_size)
        self.use_integer_scaling = True
        self.use_smooth = False


class ScreenRetroFill(ScreenFill):
    """Based on ScreenFill-object. With a blocky retro-style."""

    def __init__(self, canvas_size: tuple[int, int]) -> None:
        super().__init__(canvas_size)
        self.use_integer_scaling = False
        self.use_smooth = False


class ScreenModernContain(ScreenContain):
    """Based on ScreenContain-object. With a modern smooth-style."""

    def __init__(self, canvas_size: tuple[int, int]) -> None:
        super().__init__(canvas_size)
        self.use_integer_scaling = False
        self.use_smooth = True


class ScreenModernCover(ScreenCover):
    """Based on ScreenCover-object. With a modern smooth-style."""

    def __init__(self, canvas_size: tuple[int, int]) -> None:
        super().__init__(canvas_size)
        self.use_integer_scaling = False
        self.use_smooth = True


class ScreenModernFill(ScreenFill):
    """Based on ScreenFill-object. With a modern smooth-style."""

    def __init__(self, canvas_size: tuple[int, int]) -> None:
        super().__init__(canvas_size)
        self.use_integer_scaling = False
        self.use_smooth = True
