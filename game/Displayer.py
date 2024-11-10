import pygame

from game.Common import TILES_PER_ROW, TITLE_BAR_SIZE_IN_PIXELS


class Displayer:
    def __init__(self):
        pygame.init()
        info = pygame.display.Info()
        pygame.display.set_caption("Sokoban")

        self.display_font = pygame.font.Font(None, 36)
        self.display_width, self.display_height = info.current_w, info.current_h - TITLE_BAR_SIZE_IN_PIXELS
        self.display = pygame.display.set_mode((self.display_width,  self.display_height), pygame.RESIZABLE)

        self.tile_size = min(self.display_width // TILES_PER_ROW, (self.display_height - 100) // TILES_PER_ROW)

        self.tile_grid_width = self.tile_size * TILES_PER_ROW
        self.tile_grid_height = self.tile_size * TILES_PER_ROW

        self.left_corner_x_coordinate = (self.display_width - self.tile_grid_width) // 2
        self.left_corner_y_coordinate = (self.display_height - self.tile_grid_height) // 2

        self.soldier = pygame.image.load("images/soldier.png")
        self.soldier = pygame.transform.scale(self.soldier, (self.tile_size, self.tile_size))

    def get_left_corner_coordinates(self):
        return self.left_corner_x_coordinate, self.left_corner_y_coordinate

    def get_tile_size(self):
        return self.tile_size

    def display_soldier_on_position(self, soldier_position):
        self.display.blit(self.soldier, soldier_position)

    def display_soldier_in_the_center(self):
        return pygame.Vector2(self.display.get_width() / 2 - self.tile_size / 2, self.display.get_height() / 2 - self.tile_size / 2)

    def display_score(self, score):
        score_text = self.display_font.render(f"Score: {score}", True, (255, 255, 255))
        self.display.blit(score_text, (10, 10))

        if score == 100:
            self.display.blit(self.display_font.render("You win!", True, (255, 255, 255)), (10, 40))

    def display_level(self, level):
        bomb, bricks, chest, grass = self.load_images()

        grass = pygame.transform.scale(grass, (self.tile_size, self.tile_size))
        bricks = pygame.transform.scale(bricks, (self.tile_size, self.tile_size))
        bomb = pygame.transform.scale(bomb, (self.tile_size, self.tile_size))
        chest = pygame.transform.scale(chest, (self.tile_size, self.tile_size))

        for y, row in enumerate(level):
            for x, tile in enumerate(row):
                tile_x_coordinate = self.left_corner_x_coordinate + x * self.tile_size
                tile_y_coordinate = self.left_corner_y_coordinate + y * self.tile_size

                if tile == 1:
                    self.display.blit(bricks, (tile_x_coordinate, tile_y_coordinate))
                elif tile == 2:
                    self.display.blit(chest, (tile_x_coordinate, tile_y_coordinate))
                elif tile == 3:
                    self.display.blit(bomb, (tile_x_coordinate, tile_y_coordinate))
                else:
                    self.display.blit(grass, (tile_x_coordinate, tile_y_coordinate))

    def flip(self):
        pygame.display.flip()

    def load_images(self):
        bricks = pygame.image.load("images/bricks.png")
        grass = pygame.image.load("images/floor.png")
        bomb = pygame.image.load("images/bomb.png")
        chest = pygame.image.load("images/chest.png")
        return bomb, bricks, chest, grass

    def fill_display_with_color(self, color):
        self.display.fill(color)

