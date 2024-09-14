import pygame

# Define a custom event for triggering the flag flashing effect
flash_event = pygame.USEREVENT + 1

class Flag:
    def __init__(self, screen):
        self.screen = screen
        self.width = 400
        self.height = 50
        self.rect = pygame.Rect(0, 0, self.width, self.height)
        self.rect.midtop = screen.get_rect().midtop
        self.default_color = (255, 255, 255)
        self.colors = [(255, 255, 255), (255, 255, 0), (128, 0, 128)]
        self.current_color_index = 0
        self.flashing = False
        self.flash_duration = 2000
        self.flash_interval = 50
        self.flash_start_time = 0

    def flash(self):
        """Activates the flashing effect and starts the timer for color transitions."""
        self.flashing = True
        self.flash_start_time = pygame.time.get_ticks()
        pygame.time.set_timer(flash_event, self.flash_interval)

    def stop_flashing(self):
        """Stops the flashing effect and resets the timer."""
        self.flashing = False
        pygame.time.set_timer(flash_event, 0)

    def update(self):
        """Updates the flag status."""
        if self.flashing:
            current_time = pygame.time.get_ticks()
            if current_time - self.flash_start_time >= self.flash_duration:
                self.stop_flashing()

    def handle_event(self, event):
        """Cycles through colors when flashing is active."""
        if event.type == flash_event and self.flashing:
            self.current_color_index = (self.current_color_index + 1) % len(self.colors)

    def draw(self):
        """Draws flag on screen."""
        color = self.default_color if not self.flashing else self.colors[self.current_color_index]
        square_size = 13
        for y in range(0, self.height - square_size, square_size):
            for x in range(0, self.width, square_size):
                rect = pygame.Rect(self.rect.x + x, self.rect.y + y, square_size, square_size)
                pygame.draw.rect(self.screen, color if (x // square_size + y // square_size) % 2 == 0 else (0, 0, 0),
                                 rect)
