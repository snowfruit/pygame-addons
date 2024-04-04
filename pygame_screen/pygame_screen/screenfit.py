import math
import pygame
from .screen import *

# Naming is done by matching css naming conventions.
# Reference: https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit


class ScreenContain(Screen):
    """Based on Screen-object. Applies a contain-style to canvas-surface.
    Note:
        https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit#contain
    """

    def __init__(self, canvas_size: tuple[int, int]) -> None:
        super().__init__(canvas_size)

    def update(self) -> None:
        self.update_scale()
        self.update_position()

    def update_scale(self) -> None:
        super().update_scale()

        # Modify scale to contain inside screen-surface.
        if self.use_integer_scaling:
            self.scale_x = math.floor(self.scale_x)
            self.scale_y = math.floor(self.scale_y)

        # Set scale to the smallest of width and height.
        self.scale = min(self.scale_x, self.scale_y)

        # Set scale to a minimum of 1.
        self.scale = max(self.scale, 1)

        # 'contain' mouse needs scale_x and scale_y to be the same as scale.
        self.scale_x = self.scale
        self.scale_y = self.scale


class ScreenFill(Screen):
    """Based on Screen-object. Applies a fill-style to canvas-surface.
    Note:
        https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit#fill
    """

    def __init__(self, canvas_size: tuple[int, int]) -> None:
        super().__init__(canvas_size)

    def update(self) -> None:
        self.update_scale()
        self.update_position()

    def update_scale(self) -> None:
        super().update_scale()
        # Fill use scale_x and scale_y for mouse postion, not rendering.

        # Fill do not use 'scale'.
        self.scale = 1

    def update_position(self) -> None:
        # FILL always use 0, 0.
        self.position = (0, 0)

    def update_canvas_scaled(self) -> None:
        # Resize to new resolution.
        new_size = self.screen.get_size()

        if self.use_smooth:
            self.canvas_scaled = pygame.transform.smoothscale(self.canvas, new_size)
        else:
            self.canvas_scaled = pygame.transform.scale(self.canvas, new_size)


class ScreenCover(Screen):
    """Based on Screen-object. Applies a cover-style to canvas-surface.
    Note:
        https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit#cover
    """

    def __init__(self, canvas_size: tuple[int, int]) -> None:
        super().__init__(canvas_size)

    def update(self) -> None:
        self.update_scale()
        self.update_position()

    def update_scale(self) -> None:
        super().update_scale()

        # Scale to cover screen-surface.
        if self.use_integer_scaling:
            self.scale_x = math.ceil(self.scale_x)
            self.scale_y = math.ceil(self.scale_y)

        # Set scale to the biggest of width and height.
        self.scale = max(self.scale_x, self.scale_y)

        # Set scale to a minimum of 1.
        self.scale = max(self.scale, 1)

        # 'cover' mouse needs scale_x and scale_y to be the same as scale.
        self.scale_x = self.scale
        self.scale_y = self.scale


class ScreenMatch(Screen):
    """Based on Screen-object. With same sized canvas-surface and screen-surface."""

    def __init__(self, canvas_size: tuple[int, int]) -> None:
        super().__init__(canvas_size)

    def update(self) -> None:
        self.update_scale()
        self.update_position()

        # Make sure the canvas-surface and the screen-surface are the same size.
        if self.canvas.get_size() != self.screen.get_size():
            self.canvas = pygame.Surface(self.screen.get_size())

    def update_scale(self) -> None:
        # Match-fit use a canvas-surface and screen-surface of the same size.
        # No scaling is done.
        self.scale = 1
        self.scale_x = 1
        self.scale_y = 1

    def update_position(self) -> None:
        # Match-fit always use 0, 0.
        self.position = (0, 0)

    def update_canvas_scaled(self) -> None:
        # Match-fit use a copy of the canvas-surface. No change in size is needed.
        self.canvas_scaled = self.canvas.copy()

    def position_canvas_to_screen(self, position: tuple[int, int]) -> tuple[int, int]:
        # For match-fit the canvas-postion and screen-position are the same.
        return position

    def position_screen_to_canvas(
        self, position: tuple[int, int], clamp: bool = True
    ) -> tuple[int, int]:
        # For match-fit the canvas-postion and screen-position are the same.
        return position
