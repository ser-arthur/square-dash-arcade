import pygame
import random

car_colors = ["#40E0D0", "#008080", "#00FF7F", "#009E60", "#9FE2BF", "#999999", "#666666", "#053656"]
BASE_SPEED = 5.0

class Car:
    def __init__(self, screen, x, y, width=50, height=25, speed=BASE_SPEED, color="#40E0D0"):
        self.screen = screen
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.speed = speed
        self.color = pygame.Color(color)

    def draw(self):
        """Draws a car on the screen."""
        pygame.draw.rect(self.screen, self.color, (self.x, self.y, self.width, self.height))

    def update(self):
        """Update the car's position and respawn it if it moves off-screen."""
        self.x -= self.speed
        if self.x + self.width < 0:
            self.respawn()

    def respawn(self):
        """Respawns cars on the right side of the screen with random y-position, color and speed."""
        self.x = self.screen.get_width()
        self.y = random.randint(50, self.screen.get_height() - 70)
        self.speed = random.uniform(BASE_SPEED - 0.5, BASE_SPEED + 2.5)
        self.color = pygame.Color(random.choice(car_colors))


class CarFleet:
    def __init__(self, screen, num_cars=12):
        self.screen = screen
        self.num_cars = num_cars
        self.cars = []
        self.base_speed = BASE_SPEED
        self.create_fleet()

    def create_fleet(self):
        """Creates the initial fleet of cars."""
        for _ in range(self.num_cars):
            self.add_new_car()

    def add_new_car(self):
        """Adds a new car to the fleet from the right side of the screen."""
        screen_height = self.screen.get_height()
        screen_width = self.screen.get_width()
        car_width = 50
        car_height = 25

        x = random.randint(screen_width + 100, screen_width + 500)
        y = random.randint(50, screen_height - 70)
        speed = random.uniform(self.base_speed - 0.5, self.base_speed + 2.5)
        color = random.choice(car_colors)
        new_car = Car(self.screen, x, y, car_width, car_height, speed, color)
        self.cars.append(new_car)

    def update(self):
        """Updates the position of all cars in the fleet."""
        for car in self.cars[:]:
            car.update()

    def draw(self):
        """Draws all cars in the fleet on the screen."""
        for car in self.cars:
            car.draw()

    def increase_car_speed(self):
        """Increases car speed when leveling up."""
        global BASE_SPEED
        self.base_speed += 1
        BASE_SPEED = self.base_speed
        self.cars.clear()
        self.create_fleet()

    def reset(self):
        """Resets the car fleet to its initial state."""
        global BASE_SPEED
        BASE_SPEED = 5.0
        self.base_speed = BASE_SPEED
        self.num_cars = 12
        self.cars.clear()
        self.create_fleet()
