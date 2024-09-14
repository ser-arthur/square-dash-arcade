import pygame
import time
from player import Player
from car_fleet import CarFleet
from scoreboard import Scoreboard
from flag import Flag
from intro import run_intro


pygame.init()
screen = pygame.display.set_mode((700, 700))
pygame.display.set_caption("Square Dash")

# Game sounds
pygame.mixer.init()
sounds = {
    "level_up": pygame.mixer.Sound("sounds/level-up.wav"),
    "collision": pygame.mixer.Sound("sounds/collision.wav"),
    "game_over": pygame.mixer.Sound("sounds/game-over.wav"),
    "game_win": pygame.mixer.Sound("sounds/game-win.wav"),
    "game_start": pygame.mixer.Sound("sounds/game-start.wav"),
    "background_music": pygame.mixer.Sound("sounds/background-music.wav"),
}
channel = pygame.mixer.Channel(0)


def show_intro(screen, duration=3):
    """Queues the animation for the game title."""
    channel.play(sounds["background_music"], loops=-1)
    start_time = time.time()
    while time.time() - start_time < duration:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

        run_intro(screen)

        pygame.display.flip()
    sounds["game_start"].play()


def main_game_loop():
    flag = Flag(screen)
    car_fleet = CarFleet(screen)
    player = Player(screen, flag)
    scoreboard = Scoreboard(screen)
    clock = pygame.time.Clock()

    PLAYING, FLASH_EVENT, GAME_OVER = "playing", "flash_event", "game_over"
    game_state = PLAYING

    show_intro(screen)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if game_state == GAME_OVER and event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                reset_game(player, car_fleet, scoreboard)
                game_state = PLAYING
            if game_state == PLAYING:
                player.handle_event(event)
            elif game_state == FLASH_EVENT:
                flag.handle_event(event)

        if game_state == PLAYING:
            player.update()
            car_fleet.update()
            flag.update()

            if check_collisions(player, car_fleet, scoreboard):
                game_state = GAME_OVER

            if player.at_finish_line():
                flag.flash()
                game_state = FLASH_EVENT
                channel.pause()
                sounds["game_win"].play()

        elif game_state == FLASH_EVENT:
            flag.update()
            if not flag.flashing:
                sounds["level_up"].play()
                scoreboard.level_up()
                player.go_to_start()
                car_fleet.increase_car_speed()
                game_state = PLAYING
                channel.unpause()

        elif game_state == GAME_OVER:
            scoreboard.show_game_over()
            pygame.display.flip()

        screen.fill((0, 0, 0))
        car_fleet.draw()
        flag.draw()
        player.draw()
        scoreboard.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()


def check_collisions(player, car_fleet, scoreboard):
    """Checks for collision between player and car."""
    player_rect = pygame.Rect(player.x, player.y, player.width, player.height)
    for car in car_fleet.cars:
        car_rect = pygame.Rect(car.x, car.y, car.width, car.height)
        if player_rect.colliderect(car_rect):
            scoreboard.clear_message_area(car_fleet, player_rect)
            channel.stop()
            sounds["collision"].play()
            sounds["game_over"].play()
            return True
    return False


def reset_game(player, car_fleet, scoreboard):
    player.go_to_start()
    car_fleet.reset()
    scoreboard.reset_score()
    channel.play(sounds["background_music"], loops=-1)
    sounds["game_start"].play()


if __name__ == "__main__":
    main_game_loop()
