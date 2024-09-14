import pygame
import time


pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Square Dash")
clock = pygame.time.Clock()

background_color = (0, 0, 0)
title_color = (81, 204, 223)
square_colors = [(7, 90, 131), (202, 201, 205)]
colors = ["#00FF7F", "#008080", "#999999", "#40E0D0", "#FFEC46",  "#B877EE", "#FFDAB9", "#009E60", "#9FE2BF", "#C5BA58"]


def dash_squares(screen, square_size=25):
    """Shows 2 squares dashing vertically across the screen."""
    speed = 9
    top_square_x = 370
    top_square_y = 330
    bottom_square_x = 300
    bottom_square_y = 370

    while top_square_y > 50 or bottom_square_y < 50:
        screen.fill(background_color)

        if top_square_y > 0:
            top_square_y -= speed
            pygame.draw.rect(screen, square_colors[0], (top_square_x, top_square_y, square_size, square_size))
        if bottom_square_y < 700:
            bottom_square_y += speed
            pygame.draw.rect(screen, square_colors[1], (bottom_square_x, bottom_square_y, square_size, square_size))

        pygame.display.flip()
        clock.tick(60)


def flash_title(screen, text, font, flash_colors):
    """Flashes the title with different colors."""
    start_time = time.time()
    flash_duration = 3
    flash_speed = 0.1
    color_index = 0

    while time.time() - start_time < flash_duration:
        screen.fill(background_color)

        flash_color = pygame.Color(flash_colors[color_index % len(flash_colors)])
        title_surface = font.render(text, True, flash_color)
        screen.blit(title_surface, title_surface.get_rect(center=(350, 350)))

        pygame.display.flip()
        clock.tick(60)

        color_index += 1
        time.sleep(flash_speed)


def fade_in_title(screen, text, font):
    """Fades in the "Square Dash" title."""
    fade_speed = 5
    max_opacity = 255
    for opacity_level in range(0, max_opacity + 1, fade_speed):
        screen.fill(background_color)
        title_surface = font.render(text, True, title_color)
        title_surface.set_alpha(opacity_level)
        screen.blit(title_surface, title_surface.get_rect(center=(350, 350)))
        pygame.display.flip()
        clock.tick(30)


def run_intro(screen):
    font = pygame.font.Font('fonts/PressStart2P-Regular.ttf', 40)

    dash_squares(screen)

    fade_in_title(screen, "SQUARE DASH", font)

    flash_title(screen, "SQUARE DASH", font, colors)


if __name__ == "__main__":
    run_intro(screen)
    pygame.quit()
