import random
from collections import deque
from enum import Enum

number_of_soldiers = 1
wall_density = 0.2
class Generator:
    def __init__(self, size, number_of_boxes):
        self.size = size
        self.number_of_boxes = number_of_boxes
        self.iteration = 1
        self.first_index = 0
        self.last_index = self.size - 1
        self.first_movement_area_index = self.first_index + 1
        self.last_movement_area_index = self.last_index - 1

        while True:
            try:
                print("Generating level...")
                print(self.iteration)
                self.iteration += 1
                self.board = self.generate_empty_board_surrounded_by_walls()
                self.generate_walls_on_random_positions()
                self.corners = self.get_corners_of_the_walls()

                self.bombs = self.generate_bombs_on_random_positions(required_number_of_bombs=number_of_boxes)
                self.boxes = self.generate_boxes_on_random_positions(required_number_of_boxes=number_of_boxes)
                self.soldier = self.generate_soldier_on_random_position()

                if self.is_solvable():
                    break

            except Exception:
                continue


    def get_board(self):
        return self.board

    def generate_empty_board_surrounded_by_walls(self):
        return [[
            Field.WALL.value if x == self.first_index or
            y == self.first_index or
            x == self.last_index or
            y == self.last_index
            else Field.AREA.value
            for x in range(self.size)]
            for y in range(self.size)]

    def get_corners_of_the_walls(self):
        corners = []

        for y in range(self.first_movement_area_index, self.last_movement_area_index + 1):
            for x in range(self.first_movement_area_index, self.last_movement_area_index + 1):
                if self.board[y][x] == Field.AREA.value:
                    for (direction_y_1, direction_x_1), (direction_y_2, direction_x_2) in [
                        (Direction.UP.value, Direction.LEFT.value),
                        (Direction.UP.value, Direction.RIGHT.value),
                        (Direction.DOWN.value, Direction.LEFT.value),
                        (Direction.DOWN.value, Direction.RIGHT.value),
                    ]:
                        if (
                                self.board[y + direction_y_1][x + direction_x_1] == Field.WALL.value and
                                self.board[y + direction_y_2][x + direction_x_2] == Field.WALL.value
                        ):
                            corners.append((y, x))
                            break
        return corners

    def get_all_empty_positions_in_movement_area(self):
        empty_positions = []
        for y in range(self.first_movement_area_index, self.last_movement_area_index + 1):
            for x in range(self.first_movement_area_index, self.last_movement_area_index + 1):
                if self.board[y][x] == Field.AREA.value:
                    empty_positions.append((y, x))
        return empty_positions

    def generate_boxes_on_random_positions(self, required_number_of_boxes):
        empty_positions = self.get_all_empty_positions_in_movement_area()
        empty_positions = [empty_position for empty_position in empty_positions if empty_position not in self.corners]
        random.shuffle(empty_positions)
        boxes_placed = set()

        while len(boxes_placed) != required_number_of_boxes:
            y, x = empty_positions.pop()
            for direction in Direction:
                direction_y, direction_x = direction.value
                new_y, new_x = y + direction_y, x + direction_x

                if self.board[new_y][new_x] == Field.WALL.value:
                    if not self.is_possible_to_push_box_away_from_neighbour_wall(new_y, new_x, direction):
                        continue

                self.board[y][x] = Field.BOX.value
                boxes_placed.add((y, x))
        return boxes_placed

    def is_possible_to_push_box_away_from_neighbour_wall(self, y, x, direction):
        counter = 0
        start = 1
        end = self.last_movement_area_index + 1
        if (
                direction == Direction.LEFT.value or
                direction == Direction.RIGHT.value
        ):
            while start != end:
                if (
                        self.board[start][x] == Field.AREA.value or
                        self.board[start][x] == Field.BOMB.value
                ):
                    counter = counter + 1
                else:
                    counter = 0
        elif (
            direction == Direction.UP.value or
            direction == Direction.DOWN.value
        ):
            while start != end:
                if(
                        self.board[y][start] == Field.AREA.value or
                        self.board[y][start] == Field.BOMB.value
                ):
                    counter = counter + 1
                else :
                    counter = 0

        return counter == self.number_of_boxes + 1


    def generate_soldier_on_random_position(self):
        empty_positions = self.get_all_empty_positions_in_movement_area()
        random.shuffle(empty_positions)

        y, x = empty_positions.pop()
        self.board[y][x] = Field.SOLDIER.value

        return y,x

    def generate_walls_on_random_positions(self):
        empty_positions = self.get_all_empty_positions_in_movement_area()
        random.shuffle(empty_positions)
        required_number_of_walls = int(len(empty_positions) * wall_density)
        walls_placed = 0

        while walls_placed < required_number_of_walls:
            y = random.randint(self.first_movement_area_index, self.last_movement_area_index)
            x = random.randint(self.first_movement_area_index, self.last_movement_area_index)

            if self.board[y][x] == Field.AREA.value:
                self.board[y][x] = Field.WALL.value

                if self.wall_placement_generates_a_loop():
                    self.board[y][x] = Field.AREA.value
                else:
                    walls_placed += 1

    def find_first_empty_field(self):
        start = None
        for y in range(self.first_movement_area_index, self.last_movement_area_index + 1):
            for x in range(self.first_movement_area_index, self.last_movement_area_index + 1):
                if self.board[y][x] == Field.AREA.value:
                    start = (y, x)
                    break
        return start

    def wall_placement_generates_a_loop(self):
        start = self.find_first_empty_field()

        visited = set()
        queue = deque([start])

        while queue:
            y, x = queue.popleft()

            if (y, x) in visited:
                continue

            visited.add((y, x))

            for direction_y, direction_x in [direction.value for direction in Direction]:
                new_y, new_x = y + direction_y, x + direction_x

                if self.board[new_y][new_x] == Field.AREA.value:
                    queue.append((new_y, new_x))

        return self.is_loop_detected(visited)

    def is_loop_detected(self, visited):
        for y in range(self.first_movement_area_index, self.last_movement_area_index + 1):
            for x in range(self.first_movement_area_index, self.last_movement_area_index + 1):
                if self.board[y][x] == Field.AREA.value and (y, x) not in visited:
                    return True
        return False

    def is_solvable(self):
        return self.is_solvable_for_all_boxes()

    def is_solvable_for_all_boxes(self):
        for box in self.boxes:
            if not self.soldier_with_a_box_can_find_path_to_a_target(self.soldier, box):
                return False
        return True

    def soldier_with_a_box_can_find_path_to_a_target(self, start_player_position, start_box_position):
        visited = set()
        queue = deque([start_box_position])

        while queue:
            box_y, box_x = queue.popleft()

            if (box_y, box_x) in self.bombs:
                return True

            visited.add((box_y, box_x))

            for direction_y, direction_x in [direction.value for direction in Direction]:
                new_box_y, new_box_x = box_y + direction_y, box_x + direction_x
                new_player_y, new_player_x = box_y - direction_y, box_x - direction_x

                if not self.is_valid_move(new_box_y, new_box_x):
                    continue
                if not self.is_valid_move(new_player_y, new_player_x):
                    continue
                if self.is_box_in_deadlock_position(new_box_y, new_box_x):
                    continue
                if not self.soldier_can_find_path_to_a_place_behind_the_box(new_player_y, new_player_x, start_player_position, (box_y, box_x)):
                    continue

                if (new_box_y, new_box_x) not in visited:
                    queue.append((new_box_y, new_box_x))
        return False

    def soldier_can_find_path_to_a_place_behind_the_box(self, target_y, target_x, current_player_position, current_box_position):
        visited = set()
        queue = deque([current_player_position])

        while queue:
            y, x = queue.popleft()

            if (y, x) == (target_y, target_x):
                return True

            visited.add((y, x))

            for direction_y, direction_x in [direction.value for direction in Direction]:
                new_y, new_x = y + direction_y, x + direction_x

                if not (
                        self.first_movement_area_index <= new_y <= self.last_movement_area_index and
                        self.first_movement_area_index <= new_x <= self.last_movement_area_index
                ):
                    continue

                if self.board[new_y][new_x] not in [Field.AREA.value, Field.BOMB.value] or (new_y, new_x) == current_box_position:
                    continue

                if (new_y, new_x) in visited:
                    continue

                queue.append((new_y, new_x))
        return False

    def is_box_in_deadlock_position(self, box_y, box_x):
        if self.board[box_y][box_x] != Field.BOMB.value:
            adjacent_walls = 0
            for direction_y, direction_x in [direction.value for direction in Direction]:
                new_y, new_x = box_y + direction_y, box_x +  direction_x
                if self.board[new_y][new_x] == Field.WALL.value:
                    adjacent_walls += 1
            if adjacent_walls >= 2:
                return True
        return False

    def is_valid_move(self, new_y, new_x):
        if not (
                self.first_movement_area_index <= new_y <= self.last_movement_area_index and
                self.first_movement_area_index <= new_x <= self.last_movement_area_index
        ):
            return False

        return (
                self.board[new_y][new_x] == Field.AREA.value or
                self.board[new_y][new_x] == Field.BOMB.value
        )

    def generate_bombs_on_random_positions(self, required_number_of_bombs):
        empty_positions = self.get_all_empty_positions_in_movement_area()
        random.shuffle(empty_positions)
        bombs = set()

        while len(bombs) != required_number_of_bombs:
            y, x = empty_positions.pop()
            if self.is_valid_bomb_position(y, x):
                self.board[y][x] = Field.BOMB.value
                bombs.add((y, x))
        return bombs

    def is_valid_bomb_position(self, y, x):
        horizontal_free = 0
        vertical_free = 0

        for direction_y, direction_x in [direction.value for direction in BombHorizontalDirectionCheck]:
            new_y, new_x = y + direction_y, x + direction_x
            if (
                    self.first_movement_area_index <= new_y <= self.last_movement_area_index and
                    self.first_movement_area_index  <= new_x <= self.last_movement_area_index and
                    (self.board[new_y][new_x] == Field.AREA.value or self.board[new_y][new_x] == Field.BOMB.value)
            ):
                horizontal_free += 1

        for direction_y, direction_x in [direction.value for direction in BombVerticalDirectionCheck]:
            new_y, new_x = y + direction_y, x + direction_x
            if (
                    0 <= new_y < self.size and
                    0 <= new_x < self.size and
                    (self.board[new_y][new_x] == Field.AREA.value or self.board[new_y][new_x] == Field.BOMB.value)
            ):
                vertical_free += 1

        if horizontal_free >= 3 and vertical_free >= 3:
            return True

        return False

class Direction(Enum):
    LEFT = (0, -1)
    UP = (-1, 0)
    DOWN = (1, 0)
    RIGHT = (0, 1)

class Field(Enum):
    AREA = 0
    WALL = 1
    BOX = 2
    BOMB = 3
    SOLDIER = 4

class BombHorizontalDirectionCheck(Enum):
    ONE_LEFT = (0, -1)
    TWO_LEFT = (0, -2)
    ONE_RIGHT = (0, 1)
    TWO_RIGHT = (0, 2)

class BombVerticalDirectionCheck(Enum):
    ONE_UP = (-1, 0)
    TWO_UP = (-2, 0)
    ONE_DOWN = (1, 0)
    TWO_DOWN = (2, 0)