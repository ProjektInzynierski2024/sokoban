import random

def put_on_random_positions(board, number_of_objects, object_type):
    objects = set()
    while len(objects) < number_of_objects:
        y, x = random.randint(1, len(board)-2), random.randint(1, len(board)-2)
        if board[y][x] == 0:
            board[y][x] = object_type
            objects.add((y, x))
    return objects

def put_boxes_on_random_positions(board, number_of_objects, object_type):
    objects = set()
    while len(objects) < number_of_objects:
        y, x = random.randint(1, len(board)-2), random.randint(1, len(board)-2)
        if board[y][x] == 0:
            board[y][x] = object_type
            objects.add((y, x))
    return objects


def put_walls_on_random_positions(board, size):
    for _ in range(size * 3 // 3):
        y, x = random.randint(1, size-2), random.randint(1, size-2)
        if board[y][x] == 0:
            board[y][x] = 1

def generate_level(size=9, num_boxes=2, complexity=1):

    board = [[1 if x == 0 or y == 0 or x == size-1 or y == size-1 else 0 for x in range(size)] for y in range(size)]

    targets = put_on_random_positions(board, num_boxes, 2)
    player = put_on_random_positions(board, 1, 4)

    put_walls_on_random_positions(board, size)

    boxes = put_boxes_on_random_positions(board, num_boxes, 3)

    return board


def is_solvable(board, targets):
    pass

def simulate_solution(game, visited, targets):
    pass


