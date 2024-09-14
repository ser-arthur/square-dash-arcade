import pygame

class Player:
    def __init__(self, screen, flag, width=25, height=25, speed=3):
        self.screen = screen
        self.flag = flag    # Reference to the flag object (finish line)
        self.width = width
        self.height = height
        self.speed = speed
        self.color = (255, 235, 59)
        self.start_x = screen.get_width() // 2 - self.width // 2
        self.start_y = screen.get_height() - self.height - 10
        self.x = self.start_x
        self.y = self.start_y
        self.rect = pygame.Rect(self.x, self.y, self.width, self.height)

        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def draw(self):
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        """Updates player's position based on movement flags."""
        if self.moving_left and self.x > 0:
            self.x -= self.speed
        if self.moving_right and self.x < self.screen.get_width() - self.width:
            self.x += self.speed
        if self.moving_down and self.y < self.screen.get_height() - self.height:
            self.y += self.speed
        if self.moving_up and self.y >= self.flag.rect.bottom:
            self.y -= self.speed
        if self.moving_up and self.y <= self.flag.rect.bottom:
            # Prevent upward movement unless the player is within the flag's bounds at the finish line
            if self.flag.rect.left <= self.x + self.width <= self.flag.rect.right + self.width:
                self.y -= self.speed

    def handle_event(self, event):
        """Handles keyboard input for player movement."""
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                self.moving_left = True
            elif event.key == pygame.K_RIGHT:
                self.moving_right = True
            elif event.key == pygame.K_UP:
                self.moving_up = True
            elif event.key == pygame.K_DOWN:
                self.moving_down = True

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT:
                self.moving_left = False
            elif event.key == pygame.K_RIGHT:
                self.moving_right = False
            elif event.key == pygame.K_UP:
                self.moving_up = False
            elif event.key == pygame.K_DOWN:
                self.moving_down = False

    def at_finish_line(self):
        """Checks if the player has reached the finish line."""
        if self.y <= 15:
            self.y -= 40   # dash the player past the finish line
            self.update()
            self.reset_movement()
            return True
        return False

    def reset_movement(self):
        self.moving_left = False
        self.moving_right = False
        self.moving_up = False
        self.moving_down = False

    def go_to_start(self):
        self.x = self.start_x
        self.y = self.start_y
        self.reset_movement()
