import math
import pygame

from pygame_screen import *


def main():
    pygame.init()
    clock = pygame.Clock()

    # Window, screen and canvas use the same size in this example.
    window_size = (320, 240)

    # Screen use a resizable window.
    # It's not necessary to create a window here but possible.
    # screen_not_needed = pygame.display.set_mode(window_size, pygame.RESIZABLE)

    # Set canvas-size to same as starting screen-size.
    # Use the screen with a retro-preset.
    screen = ScreenRetroContain(window_size)

    pygame.display.set_caption("Pygame - CustomScreen")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            # Different screen preset to try.
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    screen = ScreenRetroContain(window_size)
                if event.key == pygame.K_2:
                    screen = ScreenModernContain(window_size)
                if event.key == pygame.K_3:
                    screen = ScreenRetroCover(window_size)
                if event.key == pygame.K_4:
                    screen = ScreenModernCover(window_size)
                if event.key == pygame.K_5:
                    screen = ScreenRetroFill(window_size)
                if event.key == pygame.K_6:
                    screen = ScreenModernFill(window_size)
                if event.key == pygame.K_7:
                    screen = ScreenMatch(window_size)

                print(screen.__class__.__name__)

        # Update the screen. Size, scale and everything else.
        screen.update()

        # Fill canvas-surface and screen-surface with set colors.
        screen.clear()

        # Render a circle to help demonstrate the scaling.
        pygame.draw.circle(screen.canvas, (255, 255, 255), (160, 120), 32)

        # Render the canvas-surface in the center of screen-surface.
        screen.blit_canvas_to_screen()

        pygame.display.flip()

        clock.tick(screen.frame_rate)
        # print(rc.get_mouse_position())

    pygame.quit()


if __name__ == "__main__":
    main()
