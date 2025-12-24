import pygame
import random
from game.maze import TILE_SIZE, MAZE_MAP, MAZE_ROWS, MAZE_COLS

class Ghost:
    def __init__(self, color=(255, 0, 0)):
        self.speed = 1.5
        self.color = color
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

        while True:
            gx = random.randint(1, MAZE_COLS - 2)
            gy = random.randint(1, MAZE_ROWS - 2)

            if MAZE_MAP[gy][gx] != "1":
                self.x = gx * TILE_SIZE
                self.y = gy * TILE_SIZE
                break

    def can_move(self, new_x, new_y):
        gx = int(new_x // TILE_SIZE)
        gy = int(new_y // TILE_SIZE)


#seçilen yer duvar değilse yani
        if MAZE_MAP[gy][gx] == "1":
            return False
        return True

    def choose_new_direction(self):
        self.direction = random.choice(["UP", "DOWN", "LEFT", "RIGHT"])

    def update(self):
        if self.direction == "UP":
            if self.can_move(self.x, self.y - self.speed):
                self.y -= self.speed
            else:
                self.choose_new_direction()

        elif self.direction == "DOWN":
            if self.can_move(self.x, self.y + self.speed):
                self.y += self.speed
            else:
                self.choose_new_direction()

        elif self.direction == "LEFT":
            if self.can_move(self.x - self.speed, self.y):
                self.x -= self.speed
            else:
                self.choose_new_direction()

        elif self.direction == "RIGHT":
            if self.can_move(self.x + self.speed, self.y):
                self.x += self.speed
            else:
                self.choose_new_direction()

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            self.color,
            (int(self.x + TILE_SIZE // 2), int(self.y + TILE_SIZE // 2)),
            TILE_SIZE // 2
        )
