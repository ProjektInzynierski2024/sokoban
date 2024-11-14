import pygame
from common.Common import TILE_SIZE

class Displayer:
    def __init__(self, game):
        self.game = game
        self.screen = pygame.display.set_mode((game.width * TILE_SIZE, game.height * TILE_SIZE))
        pygame.display.set_caption("Sokoban")

    def update_ui(self):

        bomb, bricks, chest, grass, soldier = self.load_images()

        grass = pygame.transform.scale(grass, (TILE_SIZE, TILE_SIZE))
        bricks = pygame.transform.scale(bricks, (TILE_SIZE, TILE_SIZE))
        bomb = pygame.transform.scale(bomb, (TILE_SIZE, TILE_SIZE))
        chest = pygame.transform.scale(chest, (TILE_SIZE, TILE_SIZE))
        soldier = pygame.transform.scale(soldier, (TILE_SIZE, TILE_SIZE))

        for y, row in enumerate(self.game.board):
            for x, tile in enumerate(row):
                tile_x, tile_y = x * TILE_SIZE, y * TILE_SIZE
                if tile == 1:
                    self.screen.blit(bricks, (tile_x, tile_y))
                elif tile == 2:
                    self.screen.blit(chest, (tile_x, tile_y))
                elif tile == 3:
                    self.screen.blit(bomb, (tile_x, tile_y))
                elif tile == 4:
                    self.screen.blit(soldier, (tile_x, tile_y))
                else:
                    self.screen.blit(grass, (tile_x, tile_y))

        pygame.display.flip()

    def load_images(self):
        bricks = pygame.image.load("../common/images/bricks.png")
        grass = pygame.image.load("../common/images/floor.png")
        bomb = pygame.image.load("../common/images/bomb.png")
        chest = pygame.image.load("../common/images/chest.png")
        soldier = pygame.image.load("../common/images/soldier.png")
        return bomb, bricks, chest, grass, soldier