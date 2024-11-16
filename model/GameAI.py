import sys

import pygame

from common.Common import SPEED, LEVEL
from common.Displayer import Displayer
from enum import Enum


class GameAI:
    def __init__(self, level_board):
        self.board = level_board
        self.player_position = self.get_player_position()
        self.width = len(self.board[0])
        self.height = len(self.board)
        self.targets = self.get_targets_positions()
        self.score = 0


    def get_player_position(self):
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile == 4:
                    return y, x

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

    def check_all_boxes_on_targets(self):
        return all(tile == 2 for _, tile in zip(self.targets, [self.board[x][y] for x, y in self.targets]))

    def check_any_box_on_target(self):
        return any(self.board[x][y] == 2 for x, y in self.targets)

    def play_step(self, move):
        if move == Move.UP.value:
            self.move(Direction.UP.value)
        elif move == Move.DOWN.value:
            self.move(Direction.DOWN.value)
        elif move == Move.LEFT.value:
            self.move(Direction.LEFT.value)
        elif move == Move.RIGHT.value:
            self.move(Direction.RIGHT.value)

        reward = self.check_any_box_on_target()
        done = self.check_all_boxes_on_targets()

        if reward:
            self.score += 10

        return reward, done, self.score

    def reset(self, level_board):
        self.board = level_board
        self.player_position = self.get_player_position()
        self.targets = self.get_targets_positions()

# if __name__ == "__main__":
#     clock = pygame.time.Clock()
#     game = GameAI(LEVEL)
#     displayer = Displayer(game)
#
#     while True:
#         game_over = game.play_step()
#         if game_over:
#             break
#         clock.tick(SPEED)
#
#     pygame.quit()
#     sys.exit()

class Move(Enum):
    LEFT = [1,0,0,0]
    UP = [0,1,0,0]
    DOWN = [0,0,1,0]
    RIGHT = [0,0,0,1]

class Direction(Enum):
    LEFT = (0, -1)
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)