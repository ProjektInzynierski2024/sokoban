import sys
import pygame

from common.Common import SPEED
from common.Displayer import Displayer
from generator.Generator import Generator

class Game:
    def __init__(self, level_board):
        self.initial_board = [row[:] for row in level_board]
        self.board = [row[:] for row in level_board]
        self.player_position = self.get_player_position()
        self.width = len(self.board[0])
        self.height = len(self.board)
        self.targets = self.get_targets_positions()
        self.is_completed = False
        self.score = 0

    def reset_game(self):
        self.board = [row[:] for row in self.initial_board]
        self.player_position = self.get_player_position()
        self.is_completed = False

    def get_player_position(self):
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile == 4:
                    return y, x

    def get_targets_positions(self):
        return [(y, x) for y, row in enumerate(self.board) for x, tile in enumerate(row) if tile == 3]

    def move(self, direction):
        y, x = self.player_position
        direction_y, direction_x = direction
        new_y, new_x = y + direction_y, x + direction_x
        next_y, next_x = y + 2 * direction_y, x + 2 * direction_x

        if self.is_valid(new_y, new_x):
            if self.board[new_y][new_x] == 0 or self.board[new_y][new_x] == 3:
                self.move_to_empty_or_target(new_x, new_y, x, y)
            elif self.board[new_y][new_x] == 2 and self.is_valid(next_y, next_x):
                self.move_box(new_x, new_y, next_x, next_y, x, y)

    def move_to_empty_or_target(self, new_x, new_y, x, y):
        self.board[y][x] = 0 if (y, x) not in self.targets else 3
        self.board[new_y][new_x] = 4
        self.player_position = (new_y, new_x)

    def move_box(self, new_x, new_y, next_x, next_y, x, y):
        if self.board[next_y][next_x] in (0, 3):
            self.board[y][x] = 0 if (y, x) not in self.targets else 3
            self.board[new_y][new_x] = 4
            self.board[next_y][next_x] = 2
            self.player_position = (new_y, new_x)

    def is_valid(self, y, x):
        return 0 <= y < len(self.board) and 0 <= x < len(self.board[0])

    def check_boxes_on_targets(self):
        return all(tile == 2 for _, tile in zip(self.targets, [self.board[x][y] for x, y in self.targets]))

    def play_step(self, score):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.move((-1, 0))
                elif event.key == pygame.K_DOWN:
                    self.move((1, 0))
                elif event.key == pygame.K_LEFT:
                    self.move((0, -1))
                elif event.key == pygame.K_RIGHT:
                    self.move((0, 1))
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if displayer.try_again_button.collidepoint(event.pos):
                    self.reset_game()

        self.is_completed = self.check_boxes_on_targets()
        displayer.update_ui(score)

        return self.is_completed

def initialize_game(number_of_boxes):
    generator = Generator(size=9, number_of_boxes=number_of_boxes)
    level = generator.get_board()
    game = Game(level)
    displayer = Displayer(game)
    return game, displayer, generator

if __name__ == "__main__":
    pygame.init()
    score = 0
    number_of_boxes = 1
    game, displayer, generator = initialize_game(number_of_boxes)
    clock = pygame.time.Clock()

    while True:
        game_over = game.play_step(score)

        if game_over:
            score += 1
            displayer.update_ui(score)
            if score % 5 == 0:
                number_of_boxes += 1
            pygame.time.wait(3000)
            game, displayer, generator = initialize_game(number_of_boxes)
        if score == 25:
            pygame.quit()
            sys.exit()
        displayer.update_ui(score)
        clock.tick(SPEED)