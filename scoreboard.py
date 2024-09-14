import pygame
import time


class Scoreboard:
    def __init__(self, screen):
        self.screen = screen
        self.level = 1
        self.text_color = (255, 236, 70)
        self.game_over = False
        self.flashing_active = False

        self.level_font = pygame.font.Font("fonts/Anta-Regular.ttf", 22)
        self.level_up_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 33)
        self.game_over_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 35)
        self.restart_font = pygame.font.Font("fonts/PressStart2P-Regular.ttf", 15)

        level_str = f"LVL: {self.level}"
        self.level_image = self.level_font.render(level_str, True, self.text_color)
        self.level_rect = self.level_image.get_rect(topleft=(20, 5))

        self.game_over_image = self.game_over_font.render(
            "GAME OVER", True, (255, 0, 0)
        )
        self.game_over_rect = self.game_over_image.get_rect()
        self.game_over_rect.center = (
            self.screen.get_rect().centerx,
            self.screen.get_rect().centery - 50,
        )

        self.restart_image = self.restart_font.render(
            "Press ENTER to restart", True, (128, 63, 231)
        )
        self.restart_rect = self.restart_image.get_rect()
        self.restart_rect.center = (
            self.screen.get_rect().centerx,
            self.screen.get_rect().centery + 30,
        )

    def update_level_image(self):
        """Updates the level text image when the level changes."""
        level_str = f"LVL: {self.level}"
        self.level_image = self.level_font.render(level_str, True, self.text_color)
        self.level_rect = self.level_image.get_rect(topleft=(20, 5))

    def draw(self):
        """Draws the current level and game over message on the screen."""
        self.screen.blit(self.level_image, self.level_rect)
        if self.game_over:
            self.show_game_over()

    def level_up(self):
        """Increases the level and displays a level-up message."""
        self.level += 1
        self.update_level_image()
        self.show_level_up_message()

    def show_level_up_message(self):
        """Displays the level-up message for 2 seconds."""
        message = f"Level {self.level}"
        message_image = self.level_up_font.render(message, True, self.text_color)
        message_rect = message_image.get_rect(center=self.screen.get_rect().center)

        self.screen.fill((0, 0, 0))
        self.screen.blit(message_image, message_rect)
        pygame.display.flip()
        pygame.time.delay(2000)

    def toggle_game_over_flash(self):
        if not self.game_over:
            self.flashing_active = True

    def show_game_over(self):
        """Displays the game over message and restart prompt."""
        self.toggle_game_over_flash()
        if self.flashing_active:
            start_time = time.time()
            flash_duration = 2
            flash_interval = 0.5

            # Flash the game over message
            while time.time() - start_time < flash_duration:
                if int((time.time() - start_time) // flash_interval) % 2 == 0:
                    self.screen.blit(self.game_over_image, self.game_over_rect)
                else:
                    self.screen.fill((0, 0, 0), self.game_over_rect)
                pygame.display.flip()
                pygame.time.delay(int(flash_interval * 1000))

        self.game_over = True
        self.flashing_active = False
        self.screen.blit(self.game_over_image, self.game_over_rect)
        self.screen.blit(self.restart_image, self.restart_rect)
        pygame.display.flip()

    def clear_message_area(self, car_fleet, player):
        """Removes cars that overlap with the 'GAME OVER' message area."""
        message_area_rect = self.game_over_rect.union(self.restart_rect)

        for car in car_fleet.cars[:]:
            car_rect = pygame.Rect(car.x, car.y, car.width, car.height)
            if car_rect.colliderect(message_area_rect) and not player.colliderect(
                message_area_rect
            ):
                car_fleet.cars.remove(car)

    def reset_score(self):
        """Resets the level and game over state."""
        self.level = 1
        self.game_over = False
        self.flashing_active = False
        self.update_level_image()
