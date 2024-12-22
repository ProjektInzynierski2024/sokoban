import random
from collections import deque
import heapq

class Generator:
    def __init__(self, size, number_of_boxes):
        self.size = size
        self.number_of_boxes = number_of_boxes
        self.iteration = 1

        while True:
            print("Generating level...")
            print(self.iteration)
            self.iteration += 1
            self.board = self.generate_board()
            self.put_walls_on_random_positions()
            self.corners = self.get_corners()
            self.targets = self.put_on_random_positions(number_of_objects=number_of_boxes, object_type=3)
            self.boxes = self.put_boxes_on_random_positions(number_of_objects=number_of_boxes, object_type=2)
            self.player = self.put_on_random_positions(number_of_objects=1, object_type=4)

            if self.is_solvable():
                print(self.board)
                break

    def get_board(self):
        return self.board

    def generate_board(self):
        return [[1 if x == 0 or y == 0 or x == self.size - 1 or y == self.size - 1 else 0 for x in range(self.size)] for
                y in range(self.size)]

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

    def get_empty_positions(self):
        empty_positions = []
        for y in range(1, len(self.board) - 1):
            for x in range(1, len(self.board[y]) - 1):
                if self.board[y][x] == 0:
                    empty_positions.append((y, x))
        return empty_positions

    def put_on_random_positions(self, number_of_objects, object_type):
        empty_positions = self.get_empty_positions()
        random.shuffle(empty_positions)
        objects = set()
        for i in range(number_of_objects):
            y, x = empty_positions[i]
            self.board[y][x] = object_type
            objects.add((y, x))
        return objects

    def put_boxes_on_random_positions(self, number_of_objects, object_type):
        empty_positions = self.get_empty_positions()
        random.shuffle(empty_positions)
        objects = set()
        i = 0
        while len(objects) < number_of_objects and i < len(empty_positions):
            y, x = empty_positions[i]
            if (y, x) not in self.corners:
                self.board[y][x] = object_type
                objects.add((y, x))
            i += 1
        return objects

    def put_walls_on_random_positions(self, wall_density=0.3):
        total_cells = (self.size - 2) ** 2
        target_walls = int(total_cells * wall_density)
        walls_added = 0

        while walls_added < target_walls:
            y, x = random.randint(1, self.size - 2), random.randint(1, self.size - 2)
            if self.board[y][x] == 0:
                self.board[y][x] = 1
                if self.is_board_connected():
                    walls_added += 1
                else:
                    self.board[y][x] = 0

    def is_board_connected(self):
        start = None
        for y in range(1, len(self.board) - 1):
            for x in range(1, len(self.board[y]) - 1):
                if self.board[y][x] == 0:
                    start = (y, x)
                    break
            if start:
                break

        if not start:
            return False

        visited = set()
        stack = [start]
        while stack:
            cy, cx = stack.pop()
            if (cy, cx) in visited:
                continue
            visited.add((cy, cx))
            for ny, nx in [(cy - 1, cx), (cy + 1, cx), (cy, cx - 1), (cy, cx + 1)]:
                if 0 <= ny < len(self.board) and 0 <= nx < len(self.board[0]) and (ny, nx) not in visited:
                    if self.board[ny][nx] == 0:
                        stack.append((ny, nx))

        for y in range(1, len(self.board) - 1):
            for x in range(1, len(self.board[y]) - 1):
                if self.board[y][x] == 0 and (y, x) not in visited:
                    return False
        return True

    def is_solvable(self):
        return self.can_solve_for_all_boxes()

    def can_solve_for_all_boxes(self):
        player = list(self.player)[0]
        for box in self.boxes:
            if not self.can_push_box(player, box):
                return False
        return True

    def can_push_box(self, start_pos, box_pos):
        visited = set()
        priority_queue = []  # Priorytetowy BFS
        heapq.heappush(priority_queue, (0, box_pos[0], box_pos[1]))

        while priority_queue:
            priority, box_y, box_x = heapq.heappop(priority_queue)

            if (box_y, box_x) in self.targets:
                return True

            visited.add((box_y, box_x))

            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                new_box_y, new_box_x = box_y + dy, box_x + dx
                player_y, player_x = box_y - dy, box_x - dx

                if not self.is_valid_box_move(new_box_y, new_box_x):
                    continue

                if not self.can_player_reach(player_y, player_x, start_pos):
                    continue

                if (new_box_y, new_box_x) not in visited:
                    distance_to_target = min(abs(t[0] - new_box_y) + abs(t[1] - new_box_x) for t in self.targets)
                    heapq.heappush(priority_queue, (distance_to_target, new_box_y, new_box_x))

        return False

    def can_player_reach(self, target_y, target_x, start_pos):
        visited = set()
        queue = deque([start_pos])

        while queue:
            y, x = queue.popleft()

            if (y, x) == (target_y, target_x):
                return True

            visited.add((y, x))

            for dy, dx in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                ny, nx = y + dy, x + dx
                if (0 <= ny < self.size and 0 <= nx < self.size and
                        self.board[ny][nx] == 0 and (ny, nx) not in visited):
                    queue.append((ny, nx))

        return False

    def is_valid_box_move(self, new_box_y, new_box_x):
        if not (0 <= new_box_y < self.size - 2 and 0 <= new_box_x < self.size - 2):
            return False
        return self.board[new_box_y][new_box_x] == 0 or self.board[new_box_y][new_box_x] == 3
