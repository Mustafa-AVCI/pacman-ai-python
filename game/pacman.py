import pygame
from game.maze import TILE_SIZE, MAZE_MAP

class Pacman:
    def __init__(self):
        self.grid_x = 14
        self.grid_y = 17

        self.x = self.grid_x * TILE_SIZE
        self.y = self.grid_y * TILE_SIZE

        self.speed = 2
        self.direction = None
        self.radius = TILE_SIZE // 2 - 2


    def at_tile_center(self):
        return (self.x % TILE_SIZE == 0) and (self.y % TILE_SIZE == 0)

    def can_move_grid(self, gx, gy):
        if gy < 0 or gy >= len(MAZE_MAP):
            return False
        if gx < 0 or gx >= len(MAZE_MAP[0]):
            return False

        # Eğer hedef hücre duvar değilse hareket edebilir yoksa edemz
        return MAZE_MAP[gy][gx] != "1"

    def can_move_direction(self, direction):
        gx, gy = self.grid_x, self.grid_y
        if direction == "UP":
            gy -= 1
        elif direction == "DOWN":
            gy += 1
        elif direction == "LEFT":
            gx -= 1
        elif direction == "RIGHT":
            gx += 1
        else:
            return False

        return self.can_move_grid(gx, gy)


    def handle_input(self):
        if not self.at_tile_center():
            return

        keys = pygame.key.get_pressed()

        if keys[pygame.K_UP] and self.can_move_direction("UP"):
            self.direction = "UP"
        elif keys[pygame.K_DOWN] and self.can_move_direction("DOWN"):
            self.direction = "DOWN"
        elif keys[pygame.K_LEFT] and self.can_move_direction("LEFT"):
            self.direction = "LEFT"
        elif keys[pygame.K_RIGHT] and self.can_move_direction("RIGHT"):
            self.direction = "RIGHT"


    def ai_move(self, best_direction):
        if self.at_tile_center() and self.can_move_direction(best_direction):
            self.direction = best_direction


    def update(self):
        if self.direction is None:
            return

        if self.direction == "UP":
            if self.at_tile_center():
                if not self.can_move_direction("UP"):
                    return
            self.y -= self.speed

        elif self.direction == "DOWN":
            if self.at_tile_center():
                if not self.can_move_direction("DOWN"):
                    return
            self.y += self.speed

        elif self.direction == "LEFT":
            if self.at_tile_center():
                if not self.can_move_direction("LEFT"):
                    return
            self.x -= self.speed

        elif self.direction == "RIGHT":
            if self.at_tile_center():
                if not self.can_move_direction("RIGHT"):
                    return
            self.x += self.speed

        self.grid_x = self.x // TILE_SIZE
        self.grid_y = self.y // TILE_SIZE

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (255, 255, 0),
            (int(self.x + TILE_SIZE // 2), int(self.y + TILE_SIZE // 2)),
            self.radius
        )
