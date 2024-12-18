import sys

import pygame

from common.Common import SPEED, LEVEL
from common.Displayer import Displayer
from enum import Enum


class GameAI:
    def __init__(self, level_board):
        self.original_board = [row[:] for row in level_board]
        self.board = [row[:] for row in level_board]
        self.player_position = self.get_player_position()
        self.width = len(self.board[0])
        self.height = len(self.board)
        self.targets = self.get_targets_positions()
        self.corners = self.get_corners()
        self.visited_positions = set()
        self.total_moves = 0
        self.total_reward = 0
        self.max_moves = 20

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

    def get_corners(self):
        corners = []
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if self.board[y][x] == 0 and (
                        (self.board[y - 1][x] == 1 and self.board[y][x - 1] == 1) or
                        (self.board[y - 1][x] == 1 and self.board[y][x + 1] == 1) or
                        (self.board[y + 1][x] == 1 and self.board[y][x - 1] == 1) or
                        (self.board[y + 1][x] == 1 and self.board[y][x + 1] == 1)
                ):
                    corners.append((y, x))
        return corners

    def move(self, direction):
        y, x = self.player_position
        direction_y, direction_x = direction

        new_y, new_x = y + direction_y, x + direction_x
        next_y, next_x = y + 2 * direction_y, x + 2 * direction_x

        reward = 0
        if self.is_valid(new_y, new_x):
            if self.board[new_y][new_x] == 0 or self.board[new_y][new_x] == 3:
                self.board[y][x] = 0 if (y, x) not in self.targets else 3
                self.board[new_y][new_x] = 4
                self.player_position = (new_y, new_x)
            elif self.board[new_y][new_x] == 2 and self.is_valid(next_y, next_x):
                if self.board[next_y][next_x] in (0, 3):
                    self.board[y][x] = 0 if (y, x) not in self.targets else 3
                    self.board[new_y][new_x] = 4
                    self.board[next_y][next_x] = 2
                    self.player_position = (new_y, new_x)
                    reward += 1
        # else:
        #     reward -= 1

        # Kara za odwiedzenie tej samej pozycji
        # if self.player_position in self.visited_positions:
        #     reward -= 0.1
        # else:
        #     self.visited_positions.add(self.player_position)

        return reward

    def calculate_total_distance(self):
        total_distance = 0
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile == 2:  # Skrzynia
                    min_distance = float('inf')
                    for target_y, target_x in self.targets:
                        distance = abs(y - target_y) + abs(x - target_x)
                        min_distance = min(min_distance, distance)
                    total_distance += min_distance
        return total_distance

    def adjust_reward_based_on_distance(self, previous_distance):
        # Zabezpieczenie przed błędami związanymi z niemożliwością obliczenia odległości
        try:
            current_distance = self.calculate_total_distance()
            if current_distance < previous_distance:
                return 3
            elif current_distance > previous_distance:
                return -1.5
            return 0
        except Exception as e:
            return 0

    def is_valid(self, y, x):
        return 0 <= y < len(self.board) and 0 <= x < len(self.board[0])

    def check_all_boxes_on_targets(self):
        return all(self.board[x][y] == 2 for x, y in self.targets)

    def check_box_stuck_in_corner(self):
        for corner in self.corners:
            x, y = corner
            if self.board[x][y] == 2 and (x, y) not in self.targets:
                return True
        return False

    def play_step(self, move):
        direction_map = {
            Move.UP: Direction.UP.value,
            Move.DOWN: Direction.DOWN.value,
            Move.LEFT: Direction.LEFT.value,
            Move.RIGHT: Direction.RIGHT.value
        }
        previous_distance = self.calculate_total_distance()
        reward = self.move(direction_map[move])

        reward += self.adjust_reward_based_on_distance(previous_distance)

        self.total_reward += reward

        self.total_moves += 1

        if self.check_box_stuck_in_corner():
            self.total_reward -= 10
            return self.total_reward, True, self.total_moves

        if self.total_moves >= self.max_moves:
            self.total_reward -= 10
            return self.total_reward, True, self.total_moves

        done = self.check_all_boxes_on_targets()
        if done:
            self.total_reward += 10
            return self.total_reward, done, self.total_moves


        return self.total_reward, done, self.total_moves

    def reset(self):
        self.board = [row[:] for row in self.original_board]
        self.player_position = self.get_player_position()
        self.targets = self.get_targets_positions()
        self.total_moves = 0
        self.total_reward = 0

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