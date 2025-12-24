import math
import random
from game.maze import TILE_SIZE , MAZE_MAP  #pixel dönüşümü ve duvar kontrolü

class UtilityAI:
    def __init__(self):
        self.visited = {}

    def distance(self, x1, y1, x2, y2):
        return math.sqrt((x1 - x2) ** 2 + (y1 - y2) ** 2)
        # ana mantık Hayalet ile Pac-Man arasındak mesafeyi ölçmek

    def evaluate_direction(self, pacman, maze, ghosts, direction):
        gx, gy = pacman.grid_x, pacman.grid_y

        if direction == "UP":
            new_gx, new_gy = gx, gy - 1
        elif direction == "DOWN":
            new_gx, new_gy = gx, gy + 1
        elif direction == "LEFT":
            new_gx, new_gy = gx - 1, gy
        else:
            new_gx, new_gy = gx + 1, gy

        if new_gy < 0 or new_gy >= len(MAZE_MAP):
            return -1e9         # kötü puan veriyoruz
        if new_gx < 0 or new_gx >= len(MAZE_MAP[0]):
            return -1e9
        if MAZE_MAP[new_gy][new_gx] == "1":
            return -1e9

        utility = 0

        tile = maze.tiles[new_gy][new_gx]
        if tile == "0":
            utility += 30
        elif tile == "2":
            utility += 100

        new_x = new_gx * TILE_SIZE + TILE_SIZE // 2
        new_y = new_gy * TILE_SIZE + TILE_SIZE // 2

        min_dist = 9999
        for g in ghosts:
            dist = self.distance(new_x, new_y, g.x, g.y)
            min_dist = min(min_dist, dist)

        if min_dist < 40:
            utility -= 400
        elif min_dist < 80:
            utility -= 150
        else:
            utility += min_dist * 0.05

        visit_penalty = self.visited.get((new_gx, new_gy), 0)
        utility -= visit_penalty * 10

        opposite = {
            "UP": "DOWN",
            "DOWN": "UP",
            "LEFT": "RIGHT",
            "RIGHT": "LEFT"
        }
        if pacman.direction is not None and direction == opposite.get(pacman.direction):
            utility -= 40

        return utility

    def choose_best_direction(self, pacman, maze, ghosts):   # en iti konumu utility değeri en iyi
        directions = ["UP", "DOWN", "LEFT", "RIGHT"]

        key = (pacman.grid_x, pacman.grid_y)
        self.visited[key] = self.visited.get(key, 0) + 1   #aynı yerde dönme cezası

        scores = {}
        for d in directions:
            scores[d] = self.evaluate_direction(pacman, maze, ghosts, d) # Eğer hiç geçerli yön yoksa rastgele dön

        best_score = max(scores.values())

        valid_dirs = [d for d, s in scores.items() if s > -9000]
        if not valid_dirs:
            return random.choice(directions)

        if random.random() < 0.05:
            return random.choice(valid_dirs)

        best_direction = max(scores, key=scores.get)
        return best_direction
