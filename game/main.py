import pygame
import sys

from game.maze import Maze
from game.pacman import Pacman
from game.ghost import Ghost
from game.utility_ai import UtilityAI

pygame.init()
pygame.mixer.init()
WIDTH = 28 * 20
HEIGHT = 19 * 20

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Pac-Man AI Project")

clock = pygame.time.Clock()
font = pygame.font.SysFont("Arial", 24)

GAME_MODE = None

best_results = {
    "USER": {"score": 0, "time": None},
    "AI": {"score": 0, "time": None}
}

# Sesler
try:
    chomp_sound = pygame.mixer.Sound("assets/sounds/chomp.wav")
    power_sound = pygame.mixer.Sound("assets/sounds/power.wav")
    death_sound = pygame.mixer.Sound("assets/sounds/death.wav")
    win_sound = pygame.mixer.Sound("assets/sounds/win.wav")
except:
    chomp_sound = power_sound = death_sound = win_sound = None


def update_best_results(mode, score, t):
    data = best_results[mode]

    if score > data["score"]:
        data["score"] = score
        data["time"] = t
        return

    if score == data["score"]:
        if data["time"] is None or t < data["time"]:
            data["time"] = t


def calculate_winner():
    u = best_results["USER"]
    a = best_results["AI"]

    if u["score"] > a["score"]:
        return "USER"
    elif a["score"] > u["score"]:
        return "AI"

    if u["score"] == a["score"]:
        if u["time"] is None or a["time"] is None:
            return "None"
        if u["time"] < a["time"]:
            return "USER"
        elif a["time"] < u["time"]:
            return "AI"

    return "None"


def menu_screen():
    global GAME_MODE
    while True:
        screen.fill((0, 0, 0))

        title = font.render("PAC-MAN AI PROJECT", True, (255, 255, 0))
        user_text = font.render("1 - USER MODE", True, (255, 255, 255))
        ai_text = font.render("2 - AI MODE", True, (255, 255, 255))

        screen.blit(title, (150, 120))
        screen.blit(user_text, (200, 200))
        screen.blit(ai_text, (200, 240))

        pygame.display.flip()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_1]:
            GAME_MODE = "USER"
            return
        if keys[pygame.K_2]:
            GAME_MODE = "AI"
            return

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()


def end_screen(score, t, reason):

    update_best_results(GAME_MODE, score, t)
    winner = calculate_winner()

    while True:
        screen.fill((0, 0, 0))

        if reason == "DEATH":
            msg = font.render("GAME OVER! YOU DIED.", True, (255, 0, 0))
        else:
            msg = font.render("YOU WIN!", True, (0, 255, 0))

        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        time_text = font.render(f"Time: {t}s", True, (255, 255, 255))

        u = best_results["USER"]
        a = best_results["AI"]

        best_user = font.render(f"USER Best: {u['score']} pts | {u['time']}s", True, (0, 200, 255))
        best_ai = font.render(f"AI Best: {a['score']} pts | {a['time']}s", True, (255, 100, 0))

        winner_text = font.render(f"CURRENT WINNER: {winner}", True, (255, 255, 0))
        retry_text = font.render("Press R to Restart | Q to Quit", True, (255, 255, 0))

        screen.blit(msg, (130, 80))
        screen.blit(score_text, (200, 150))
        screen.blit(time_text, (200, 180))
        screen.blit(best_user, (120, 230))
        screen.blit(best_ai, (120, 260))
        screen.blit(winner_text, (150, 300))
        screen.blit(retry_text, (140, 340))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    return True
                if event.key == pygame.K_q:
                    return False


def start_game():
    maze = Maze()
    pacman = Pacman()
    ai = UtilityAI()

    ghosts = [
        Ghost((255, 0, 0)),
        Ghost((0, 255, 255)),
        Ghost((255, 105, 180)),
    ]

    start_time = pygame.time.get_ticks()

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if GAME_MODE == "USER":
            pacman.handle_input()

        if GAME_MODE == "AI" and pacman.at_tile_center():
            direction = ai.choose_best_direction(pacman, maze, ghosts)
            pacman.ai_move(direction)

        pacman.update()

        result = maze.eat(pacman.x, pacman.y)
        if result == "small" and chomp_sound:
            chomp_sound.play()
        elif result == "power" and power_sound:
            power_sound.play()

        for g in ghosts:
            g.update()

        for g in ghosts:
            d = ((pacman.x - g.x)**2 + (pacman.y - g.y)**2)**0.5
            if d < 15:
                elapsed = (pygame.time.get_ticks() - start_time) // 1000
                if death_sound: death_sound.play()
                return maze.score, elapsed, "DEATH"


        if maze.remaining_food() == 0:
            elapsed = (pygame.time.get_ticks() - start_time) // 1000
            if win_sound: win_sound.play()
            return maze.score, elapsed, "WIN"

        screen.fill((0, 0, 0))
        maze.draw(screen)
        pacman.draw(screen)
        for g in ghosts:
            g.draw(screen)

        screen.blit(font.render(f"Score: {maze.score}", True, (255, 255, 255)), (10, 10))
        elapsed_time = (pygame.time.get_ticks() - start_time) // 1000
        screen.blit(font.render(f"Time: {elapsed_time}s", True, (255, 255, 255)), (450, 10))

        pygame.display.flip()
        clock.tick(60)


def main():
    menu_screen()
    while True:
        score, t, reason = start_game()
        restart = end_screen(score, t, reason)
        if not restart:
            break


if __name__ == "__main__":
    main()
