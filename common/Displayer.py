import pygame
from common.Common import TILE_SIZE

class Displayer:
    def __init__(self, game, score):
        self.game = game
        self.screen = pygame.display.set_mode((game.width * TILE_SIZE, game.height * TILE_SIZE))  # Extra space for UI
        pygame.display.set_caption("Sokoban")
        self.try_again_button = pygame.Rect(5, 5, TILE_SIZE - 10, TILE_SIZE - 10)
        self.score = score

    def update_ui(self):

        bomb, bricks, chest, grass, soldier, arrow = self.load_images()

        grass = pygame.transform.scale(grass, (TILE_SIZE, TILE_SIZE))
        bricks = pygame.transform.scale(bricks, (TILE_SIZE, TILE_SIZE))
        bomb = pygame.transform.scale(bomb, (TILE_SIZE, TILE_SIZE))
        chest = pygame.transform.scale(chest, (TILE_SIZE, TILE_SIZE))
        soldier = pygame.transform.scale(soldier, (TILE_SIZE, TILE_SIZE))
        try_again_arrow = pygame.transform.scale(arrow,(TILE_SIZE - 20, TILE_SIZE - 20))

        self.screen.fill((0, 0, 0))

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

        pygame.draw.rect(self.screen, (232, 231, 227), self.try_again_button)
        self.screen.blit(try_again_arrow, (10,10))

        font = pygame.font.Font(None, 100)
        pygame.draw.rect(self.screen, (232, 231, 227), pygame.Rect(5, self.screen.get_height() - TILE_SIZE + 5, TILE_SIZE - 10, TILE_SIZE - 10))
        score_text = font.render(str(self.score), True, (0, 0, 0))
        if self.score >= 10:
            self.screen.blit(score_text, (2, self.screen.get_height() - TILE_SIZE + 10))
        else:
            self.screen.blit(score_text, (TILE_SIZE/4, self.screen.get_height() - TILE_SIZE + 10))
        pygame.display.flip()

    def load_images(self):
        bricks = pygame.image.load("common/images/bricks.png")
        grass = pygame.image.load("common/images/floor.png")
        bomb = pygame.image.load("common/images/bomb.png")
        chest = pygame.image.load("common/images/chest.png")
        soldier = pygame.image.load("common/images/soldier.png")
        arrow = pygame.image.load("common/images/arrow.png")
        return bomb, bricks, chest, grass, soldier, arrow