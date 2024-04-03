import math
from enum import Enum
import pygame

class Profile(Enum):
    NONE = 0
    RETRO_CONTAIN = 1
    RETRO_COVER = 2
    MODERN_CONTAIN = 3
    MODERN_COVER = 4
    MATCH = 5
    FILL = 6


# Reference: https://developer.mozilla.org/en-US/docs/Web/CSS/object-fit


class Fit(Enum):
    NONE = 0
    CONTAIN = 1
    FILL = 2
    COVER = 3
    MATCH = 4


class CustomCanvas:
    def __init__(self, canvas_size: tuple) -> None:
        if pygame.display.get_init() == False:
            pass

        # Fill colors.
        self.screen_color: pygame.color = (128, 0, 0)  # Dark red.
        self.canvas_color: pygame.color = (0, 128, 0)  # Dark green.

        self.screen = pygame.display.get_surface()

        self._canvas_position: tuple = (0, 0)
        self._canvas_scale = 1
        self._canvas_zoom = 1

        self.canvas: pygame.surface = pygame.Surface(canvas_size)
        self.canvas_scaled: pygame.surface = pygame.Surface(canvas_size)

        # Settings.
        self._profile: Profile = Profile.NONE
        self._clear_background: bool = True  # Clear surfaces on update.
        self._fit: Fit = Fit()  # Scaling to use for canvas-surface.
        self._smooth: bool = False  # Scale using smooth.
        # Scale using integer instead of float.
        self._integer_scaling: bool = False

    @property
    def canvas_scale(self) -> float:
        return self._canvas_scale

    @property
    def clear_background(self) -> bool:
        return self._clear_background

    @clear_background.setter
    def clear_background(self, value: bool) -> None:
        self._clear_background = value

    @property
    def smooth(self) -> bool:
        return self._smooth

    @smooth.setter
    def smooth(self, value: bool) -> None:
        self._smooth = value

    @property
    def integer_scaling(self) -> bool:
        return self._integer_scaling

    @integer_scaling.setter
    def integer_scaling(self, value: bool) -> None:
        self._integer_scaling = value

    @property
    def profile(self) -> Profile:
        return self._profile

    @profile.setter
    def profile(self, value: Profile) -> None:
        self._profile = value

        if self.profile == Profile.RETRO_COVER:
            self.smooth = False
            self.integer_scaling = True
        elif self.profile == Profile.RETRO_CONTAIN:
            self.smooth = False
            self.integer_scaling = True
        elif self.profile == Profile.MODERN_COVER:
            self.smooth = True
            self.integer_scaling = False
        elif self.profile == Profile.MODERN_CONTAIN:
            self.smooth = True
            self.integer_scaling = False
        elif self.profile == Profile.MATCH:
            # Not needed right now. Here for future use case.
            pass
        elif self.profile == Profile.FILL:
            # Not needed right now. Here for future use case.
            pass

    def clear(self) -> None:
        self.clear_canvas()
        self.clear_screen()

    def clear_canvas(self) -> None:
        self.canvas.fill(self.canvas_color)

    def clear_screen(self) -> None:
        self.screen.fill(self.screen_color)

    def is_canvas_and_screen_same_size(self) -> bool:
        if self.canvas.get_width() != self.screen.get_width():
            return False

        if self.canvas.get_height() != self.screen.get_height():
            return False

        return True

    def update_scale(self) -> None:
        # Calculate the scale-factor for the canvas-surface.
        scale_width = self.screen.get_width() / self.canvas.get_width()
        scale_height = self.screen.get_height() / self.canvas.get_height()

        if self.fit == Fit.NONE:
            # Set to self. Needed for last step.
            self.scale = self._canvas_scale
        elif self.fit == Fit.COVER:
            # Scale to cover screen-surface.
            if self.integer_scaling:
                scale_width = math.ceil(scale_width)
                scale_height = math.ceil(scale_height)

            # Set scale to the biggest of width and height.
            scale = max(scale_width, scale_height)
        elif self.fit == Fit.CONTAIN:
            # Scale to contain inside screen-surface.
            if self.integer_scaling:
                scale_width = math.floor(scale_width)
                scale_height = math.floor(scale_height)

            # Set scale to the smallest of width and height.
            scale = min(scale_width, scale_height)
        elif self.fit == Fit.FILL:
            # FILL do not use scale.
            scale = 1
        elif self.fit == Fit.MATCH:
            scale = 1
        else:
            # TODO
            scale = 1

        # Set scale to a minimum of 1.
        self._canvas_scale = max(scale, 1)

    def update(self) -> None:
        # Clear canvas-surface and screen-surface.
        if self.clear_background:
            self.clear()

        self.update_scale()

        # Get the center-position for the screen-surface.
        screen_center_x, screen_center_y = self.screen.get_rect().center

        # Get the center-position for the canvas-surface.
        canvas_center_x, canvas_center_y = self.canvas.get_rect().center

        # Add the wanted scale.
        canvas_center_x *= self._canvas_scale
        canvas_center_y *= self._canvas_scale

        # Calculate the new canvas-position.
        canvas_x: int = screen_center_x - canvas_center_x
        canvas_y: int = screen_center_y - canvas_center_y

        self._canvas_position = (canvas_x, canvas_y)

    def blit_canvas_to_screen(self) -> None:
        if self.fit == Fit.FILL:
            # Resize to new resolution.
            if self.smooth:
                self.canvas_scaled = pygame.transform.smoothscale(
                    self.canvas, self.screen.get_size())
            else:
                self.canvas_scaled = pygame.transform.scale(
                    self.canvas, self.screen.get_size()
                )
        else:
            # Resize to new resolution, using scalar(s).
            if self.smooth:
                self.canvas_scaled = pygame.transform.smoothscale_by(
                    self.canvas, self._canvas_scale
                )
            else:
                self.canvas_scaled = pygame.transform.scale_by(
                    self.canvas, self._canvas_scale
                )

        # Draw the canvas-surface the center of the screen-surface.
        self.screen.blit(self.canvas_scaled, self._canvas_position)

    def get_mouse_position(self, clamp: bool = True) -> tuple:
        position: tuple = self.position_screen_to_canvas(
            pygame.mouse.get_pos())

        return position

    def position_canvas_to_screen(self, position: tuple) -> tuple:
        # If MATCH is used the canvas-postion and screen-position are the same.
        if self.fit == Profile.MATCH:
            return position
        
        x: int = position[0] * self._canvas_scale
        y: int = position[1] * self._canvas_scale

        return (x, y)

    def position_screen_to_canvas(self, position: tuple, clamp=True) -> tuple:
        # If MATCH is used the canvas-postion and screen-position are the same.
        if self.fit == Profile.MATCH:
            return position
        
        x: int = math.floor(
            (position[0] - self._canvas_position[0]) / self._canvas_scale
        )
        y: int = math.floor(
            (position[1] - self._canvas_position[1]) / self._canvas_scale
        )

        if clamp:
            # clamp position to canvas-size.
            x = max(x, 0)
            y = max(y, 0)

            x = min(x, self.canvas.get_width())
            y = min(y, self.canvas.get_height())

        return (x, y)
