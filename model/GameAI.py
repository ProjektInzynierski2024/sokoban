import sys

import pygame

from common.Common import SPEED
from model.DisplayerAI import DisplayerAI

level = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 0, 3, 0, 0, 0, 3, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 2, 0, 2, 1, 0, 1],
        [1, 0, 0, 0, 4, 0, 0, 0, 1],
        [1, 0, 1, 2, 0, 2, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 3, 0, 0, 0, 3, 0, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

class GameAI:
    def __init__(self, level_board):
        self.board = level_board
        self.player_position = self.get_player_position()
        self.width = len(self.board[0])
        self.height = len(self.board)
        self.targets = self.get_targets_positions()


    def get_player_position(self):
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile == 4:
                    return (y, x)

    def get_targets_positions(self):
        targets = []
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile == 3:
                    targets.append((y, x))
        return targets

    def move(self, direction):
        y, x = self.player_position
        direction_y, direction_x = direction

        new_y, new_x = y + direction_y, x + direction_x
        next_y, next_x = y + 2 * direction_y, x + 2 * direction_x

        if self.is_valid(new_y, new_x):
            if self.board[new_y][new_x] == 0 or self.board[new_y][new_x] == 3:
                self.board[y][x] = 0 if (y, x) not in self.targets else 3
                self.board[new_y][new_x] = 4
                self.player_position = (new_y, new_x)
            elif self.board[new_y][new_x] == 2 and self.is_valid(next_y, next_x):
                if self.board[next_y][next_x] in (0, 3):
                    self.board[y][x] = 0 if (y, x) not in self.targets else 2
                    self.board[new_y][new_x] = 4
                    self.board[next_y][next_x] = 2
                    self.player_position = (new_y, new_x)

    def is_valid(self, y, x):
        return 0 <= y < len(self.board) and 0 <= x < len(self.board[0])

    def check_boxes_on_targets(self):
        return all(tile == 2 for _, tile in zip(self.targets, [self.board[x][y] for x, y in self.targets]))

    def play_step(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    game.move((-1, 0))
                elif event.key == pygame.K_DOWN:
                    game.move((1, 0))
                elif event.key == pygame.K_LEFT:
                    game.move((0, -1))
                elif event.key == pygame.K_RIGHT:
                    game.move((0, 1))

        displayer.update_ui()

        return game.check_boxes_on_targets()

if __name__ == "__main__":
    clock = pygame.time.Clock()
    game = GameAI(level)
    displayer = DisplayerAI(game)

    while True:
        game_over = game.play_step()
        if game_over:
            break
        clock.tick(SPEED)

    pygame.quit()
    sys.exit()


