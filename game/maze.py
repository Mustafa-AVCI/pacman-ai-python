import pygame

TILE_SIZE = 20

MAZE_MAP = [
    "1111111111111111111111111111",
    "1000000000110000000000000001",
    "1011111100110111111101111101",
    "1020000100000000000100000201",
    "1011110101110111010110111101",
    "1000000101000100010100000001",
    "1111110101110111010111111101",
    "100000000000P000000000000001",
    "1011111110110110111111111101",
    "1000000010000000001000000001",
    "1111011110110110111101111101",
    "1000010000000200000001000001",
    "1011010111110111111101101101",
    "1020010000000000000001000201",
    "1111011101110111011101111101",
    "1000000100010001000100000001",
    "1011110101110111010111111101",
    "1000000000110000000000000001",
    "1111111111111111111111111111",
]

MAZE_ROWS = len(MAZE_MAP)
MAZE_COLS = len(MAZE_MAP[0])


class Maze:
    def __init__(self):
        self.tiles = [list(row) for row in MAZE_MAP]
        self.score = 0

    def eat(self, px, py):
        gx = int(px // TILE_SIZE)
        gy = int(py // TILE_SIZE)

        tile = self.tiles[gy][gx]

        if tile == "0":
            self.tiles[gy][gx] = " "
            self.score += 10
            return "small"

        elif tile == "2":
            self.tiles[gy][gx] = " "
            self.score += 50
            return "power"

        return None

    def remaining_food(self):
        return sum(tile in ("0", "2") for row in self.tiles for tile in row)

    def draw(self, screen):
        for r, row in enumerate(self.tiles):
            for c, tile in enumerate(row):
                x = c * TILE_SIZE
                y = r * TILE_SIZE

                if tile == "1":
                    pygame.draw.rect(screen, (0, 0, 255), (x, y, TILE_SIZE, TILE_SIZE))  #mavi

                elif tile == "0":
                    pygame.draw.circle(screen, (255, 255, 0),
                        (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 3)  #sarı

                elif tile == "2":
                    pygame.draw.circle(screen, (255, 0, 0),
                        (x + TILE_SIZE // 2, y + TILE_SIZE // 2), 6)   # kırmızı
