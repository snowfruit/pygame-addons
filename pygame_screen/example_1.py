import math
import pygame

from pygame_customcanvas import *


def main():
    pygame.init()
    clock = pygame.Clock()

    # Window, screen and canvas use the same size.
    window_size = (320, 240)

    # Screen is a resizable window.
    screen = pygame.display.set_mode(window_size, pygame.RESIZABLE)

    # Set canvas-size to same as starting screen-size.
    cc = CustomCanvas(window_size)

    pygame.display.set_caption("Pygame - Retro scaling")

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        cc.update()

        # Render a circle to demonstrate the scaling.
        pygame.draw.circle(cc.canvas, (255, 255, 255), (160, 120), 32)

        # Render the canvas-surface in the center of screen-surface.
        cc.blit_canvas_to_screen()

        pygame.display.flip()

        clock.tick(30)
        # print(rc.get_mouse_position())

    pygame.quit()


if __name__ == "__main__":
    main()
