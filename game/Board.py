from Tile import Tile

class Board:
    def __init__(self, level):
        self.grid = None
        self.level = level
        self.create_board()

    def create_board(self):
        if self.level == 1:
            self.grid = [[Tile(0) for _ in range(5)] for _ in range(5)]
        elif self.level == 2:
            self.grid = [[Tile(0) for _ in range(7)] for _ in range(7)]
        elif self.level == 3:
            self.grid = [[Tile(0) for _ in range(9)] for _ in range(9)]

        self.set_boundary()

    def set_boundary(self):
        rows = len(self.grid)
        columns = len(self.grid[0]) if rows > 0 else 0

        for i in range(rows):
            for j in range(columns):
                if i == 0 or i == rows - 1 or j == 0 or j == columns - 1:
                    self.grid[i][j].set_value(2)
                else:
                    self.grid[i][j].set_value(1)

