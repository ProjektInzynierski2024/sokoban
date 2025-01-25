from enum import Enum

class GameAI:
    def __init__(self, level_board):
        self.original_board = [row[:] for row in level_board]
        self.board = [row[:] for row in level_board]
        self.player_position = self.get_player_position()
        self.width = len(self.board[0])
        self.height = len(self.board)
        self.boxes = self.get_boxes_positions()
        self.targets = self.get_targets_positions()
        self.corners = self.get_corners()
        self.visited_positions = set()
        self.total_moves = 0
        self.reward = 0
        self.max_moves = 10
        self.is_completed = False

    def get_player_position(self):
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if tile == 4:
                    return y, x

    def get_targets_positions(self):
        return [(y, x) for y, row in enumerate(self.board) for x, tile in enumerate(row) if tile == 3]

    def get_boxes_positions(self):
        return [(y, x) for y, row in enumerate(self.board) for x, tile in enumerate(row) if tile == 2]

    def get_corners(self):
        corners = []
        for y, row in enumerate(self.board):
            for x, tile in enumerate(row):
                if self.board[y][x] == 0 and self.is_corner(x, y):
                    corners.append((y, x))
        return corners

    def is_corner(self, x, y):
        return (
                (self.board[y - 1][x] == 1 and self.board[y][x - 1] == 1) or
                (self.board[y - 1][x] == 1 and self.board[y][x + 1] == 1) or
                (self.board[y + 1][x] == 1 and self.board[y][x - 1] == 1) or
                (self.board[y + 1][x] == 1 and self.board[y][x + 1] == 1)
        )

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

    def move(self, direction):
        y, x = self.player_position
        direction_y, direction_x = direction
        new_y, new_x = y + direction_y, x + direction_x
        next_y, next_x = y + 2 * direction_y, x + 2 * direction_x

        if self.is_valid(new_y, new_x):
            if self.board[new_y][new_x] == 0 or self.board[new_y][new_x] == 3:
                return self.move_to_empty_or_target(new_x, new_y, x, y)
            elif self.board[new_y][new_x] == 2 and self.is_valid(next_y, next_x):
                return self.move_box(new_x, new_y, next_x, next_y, x, y)

        return -5

    def move_to_empty_or_target(self, new_x, new_y, x, y):
        self.board[y][x] = 0 if (y, x) not in self.targets else 3
        self.board[new_y][new_x] = 4
        self.player_position = (new_y, new_x)
        return 0

    def move_box(self, new_x, new_y, next_x, next_y, x, y):
        if self.board[next_y][next_x] in (0, 3):
            self.board[y][x] = 0 if (y, x) not in self.targets else 3
            self.board[new_y][new_x] = 4
            self.board[next_y][next_x] = 2
            self.player_position = (new_y, new_x)
            return 1
        else:
            return 0

    def get_distance_between_box_and_target(self):
        box_y, box_x = self.boxes[0]
        target_y, target_x = self.targets[0]
        return abs(box_y - target_y) + abs(box_x - target_x)

    def adjust_reward_based_on_distance_box_and_target(self, previous_distance, current_distance):
        if current_distance < previous_distance:
            return 10
        elif current_distance > previous_distance:
            return -10
        else:
            return 0

    def get_distance_between_box_and_player(self):
        player_y, player_x = self.player_position
        box_y, box_x = self.boxes[0]
        return abs(box_y - player_y) + abs(box_x - player_x)

    def adjust_reward_based_on_distance_box_and_player(self, previous_distance, current_distance):
        if current_distance < previous_distance:
            return 5
        elif current_distance > previous_distance:
            return -5
        else:
            return 0

    def check_player_on_bomb(self):
        y, x = self.player_position
        if self.board[y][x] == 3:
            return -5
        else:
            return 0

    def play_step(self, move):
        direction_map = {
            Move.UP: Direction.UP.value,
            Move.DOWN: Direction.DOWN.value,
            Move.LEFT: Direction.LEFT.value,
            Move.RIGHT: Direction.RIGHT.value
        }
        reward = 0
        previous_box_and_target_distance = self.get_distance_between_box_and_target()
        previous_box_and_player_distance = self.get_distance_between_box_and_player()
        reward += self.move(direction_map[move])
        current_box_and_target_distance = self.get_distance_between_box_and_target()
        current_box_and_player_distance = self.get_distance_between_box_and_player()
        reward += self.adjust_reward_based_on_distance_box_and_target(previous_box_and_target_distance, current_box_and_target_distance)
        reward += self.adjust_reward_based_on_distance_box_and_player(previous_box_and_player_distance, current_box_and_player_distance)
        reward += self.check_player_on_bomb()
        self.total_moves += 1
        self.reward += reward
        self.boxes = self.get_boxes_positions()
        if self.check_box_stuck_in_corner() or self.total_moves >= self.max_moves:
            self.reward -= 20
            return self.reward, True, self.total_moves, False

        if self.check_all_boxes_on_targets():
            self.reward += 100
            return self.reward, True, self.total_moves, True

        return self.reward, False, self.total_moves, False

    def reset(self):
        self.board = [row[:] for row in self.original_board]
        self.player_position = self.get_player_position()
        self.targets = self.get_targets_positions()
        self.total_moves = 0
        self.reward = 0

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