import math
from enum import Enum
import pygame


class Screen:
    """Screen-object used for base. Not meant for direct use."""

    def __init__(self, canvas_size: tuple = (320, 240)) -> None:
        # Try to get available display-surface.
        self.screen = pygame.display.get_surface()

        # Create a new one if not found.
        if self.screen is None:
            self.screen = pygame.display.set_mode(canvas_size, pygame.RESIZABLE)

        self._frame_rate: float = 30.0

        # The scale-factor for the canvas-surface.
        self._scale_x: int | float = 1
        self._scale_y: int | float = 1

        # The zoom-factor for the canvas-surface.
        # TODO: Add zoom.
        self._zoom_x: int | float = 1
        self._zoom_y: int | float = 1

        # Position the canvas-surface will be rendered to on screen-surface.
        self._position: tuple[int, int] = (0, 0)

        # Scale using integer instead of float?
        self._use_integer_scaling: bool = True

        # Scale using smooth?
        self._use_smooth: bool = False

        # Fill colors.
        self._screen_color: pygame.color = (128, 0, 0)  # Dark red.
        self._canvas_color: pygame.color = (0, 128, 0)  # Dark green.

        # Set canvas-size to screen-size if 'canvas_size' is None.
        if canvas_size is None:
            canvas_size = self.screen.get_size()

        self.canvas: pygame.surface = pygame.Surface(canvas_size)
        self.canvas_scaled: pygame.surface = pygame.Surface(canvas_size)

    @property
    def frame_rate(self) -> float:
        """Only 'frame rate'-value. Does not controll the frame rate."""
        return self._frame_rate

    @frame_rate.setter
    def frame_rate(self, frame_rate: float) -> None:
        self._frame_rate = frame_rate

    @property
    def scale(self) -> tuple[int | float, int | float]:
        """Return scale_x and scale_y as tuple."""
        return (self.scale_x, self.scale_y)

    @scale.setter
    def scale(self, value: tuple[int | float, int | float]) -> None:
        self.scale_x = value[0]
        self.scale_y = value[1]

    @property
    def scale_x(self) -> int | float:
        return self._scale_x

    @scale_x.setter
    def scale_x(self, value: int | float) -> None:
        self._scale_x = value

    @property
    def scale_y(self) -> int | float:
        return self._scale_y

    @scale_y.setter
    def scale_y(self, value: int | float) -> None:
        self._scale_y = value

    @property
    def zoom(self) -> int | float:
        return self._zoom

    @zoom.setter
    def zoom(self, value: int | float) -> None:
        self._zoom = value

    @property
    def zoom_x(self) -> int | float:
        return self._zoom_x

    @zoom_x.setter
    def zoom_x(self, value: int | float) -> None:
        self._zoom_x = value

    @property
    def zoom_y(self) -> int | float:
        return self._zoom_y

    @zoom_y.setter
    def zoom_y(self, value: int | float) -> None:
        self._zoom_y = value

    @property
    def position(self) -> tuple[int, int]:
        """The position canvas-surface is rendered on screen-surface."""
        return self._position

    @position.setter
    def position(self, value: tuple[int, int]) -> None:
        self._position = value

    @property
    def use_integer_scaling(self) -> bool:
        """Resize using integer scale-values."""
        return self._use_integer_scaling

    @use_integer_scaling.setter
    def use_integer_scaling(self, value: bool) -> None:
        self._use_integer_scaling = value

    @property
    def use_smooth(self) -> bool:
        """Resize using bilinear filter on canvas-surface."""
        return self._use_smooth

    @use_smooth.setter
    def use_smooth(self, value: bool) -> None:
        self._use_smooth = value

    @property
    def canvas_color(self) -> pygame.color:
        """Color used when filling the canvas-surface when cleared."""
        return self._canvas_color

    @canvas_color.setter
    def canvas_color(self, color: pygame.color) -> None:
        self._canvas_color = color

    @property
    def screen_color(self) -> pygame.color:
        """Color used when filling the screen-surface when cleared."""
        return self._screen_color

    @screen_color.setter
    def screen_color(self, color: pygame.color) -> None:
        self._screen_color = color

    def clear(self) -> None:
        """Clear canvas-surface and screen-surface."""
        self.clear_canvas()
        self.clear_screen()

    def clear_canvas(self) -> None:
        """Clear the surface. Fills canvas-surface with set color."""
        self.canvas.fill(self.canvas_color)

    def clear_screen(self) -> None:
        """Clear the surface. Fills screen-surface with set color."""
        self.screen.fill(self.screen_color)

    def update_scale(self) -> None:
        """Update variables relavant to scale."""
        # Calculate the scale-factor for the canvas-surface.
        self.scale_x: float = self.screen.get_width() / self.canvas.get_width()
        self.scale_y: float = self.screen.get_height() / self.canvas.get_height()

    def update(self) -> None:
        """Method that calls all relevant update-methods."""
        self.update_scale()
        self.update_position()

    def update_position(self) -> None:
        """Update variables relavant to position."""
        # scale = pygame.math.Vector2(self.scale)

        # Get the center-position for the screen-surface.
        # screen_center = pygame.math.Vector2(self.screen.get_rect().center)
        screen_center_x, screen_center_y = self.screen.get_rect().center

        # Get the center-position for the canvas-surface.
        canvas_center_x, canvas_center_y = self.canvas.get_rect().center

        # Add the wanted scale.
        canvas_center_x *= self.scale_x
        canvas_center_y *= self.scale_y

        # Calculate the new canvas-position.
        # TODO: Is there a problem with rounding?
        canvas_x: int = math.floor(screen_center_x - canvas_center_x)
        canvas_y: int = math.floor(screen_center_y - canvas_center_y)

        self.position = (canvas_x, canvas_y)

    def update_canvas_scaled(self) -> None:
        """Update the canvas_scaled-surface with new size."""
        # TODO: Method needs a better name.

        # Resize to new resolution, using scalar(s).
        if self.use_smooth:
            self.canvas_scaled = pygame.transform.smoothscale_by(
                self.canvas, self.scale
            )
        else:
            self.canvas_scaled = pygame.transform.scale_by(self.canvas, self.scale)

    def blit_canvas_to_screen(self) -> None:
        """Render canvas-surface to screen-surface."""
        # Everything should be done rendering to canvas-surface by now.

        # Scale the final canvas.
        self.update_canvas_scaled()

        # Render the canvas-surface the screen-surface.
        self.screen.blit(self.canvas_scaled, self.position)

    def get_mouse_position(self, clamp: bool = True) -> tuple[int, int]:

        position: tuple[int, int] = self.position_screen_to_canvas(
            pygame.mouse.get_pos()
        )

        return position

    def position_canvas_to_screen(
        self, position: tuple, clamp: bool = True
    ) -> tuple[int, int]:
        x: int = math.floor(position[0] * self.scale_x)
        y: int = math.floor(position[1] * self.scale_y)

        return (x, y)

    def position_screen_to_canvas(
        self, position: tuple, clamp: bool = True
    ) -> tuple[int, int]:
        x: int = math.floor((position[0] - self.position[0]) / self.scale_x)
        y: int = math.floor((position[1] - self.position[1]) / self.scale_y)

        if clamp:
            # clamp position to canvas-size.
            x = max(x, 0)
            y = max(y, 0)

            x = min(x, self.canvas.get_width())
            y = min(y, self.canvas.get_height())

        return (x, y)
