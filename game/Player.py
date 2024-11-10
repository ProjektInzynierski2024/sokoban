import pygame

class Player:
    def __init__(self, start_position, tile_size, left_corner_x, left_corner_y, level_board):
        self.position = start_position
        self.tile_size = tile_size
        self.direction = None
        self.left_corner_x = left_corner_x
        self.left_corner_y = left_corner_y
        self.level_board = level_board

    def move(self):
        new_position = self.position.copy()

        keys = pygame.key.get_pressed()
        pressed_keys = [keys[pygame.K_UP], keys[pygame.K_DOWN], keys[pygame.K_LEFT], keys[pygame.K_RIGHT]]
        num_pressed_keys = sum(pressed_keys)

        if num_pressed_keys == 1:
            if keys[pygame.K_UP]:
                new_position.y -= 1 * self.tile_size
                self.direction = (0, -1)
            if keys[pygame.K_DOWN]:
                new_position.y += 1 * self.tile_size
                self.direction = (0, 1)
            if keys[pygame.K_LEFT]:
                new_position.x -= 1 * self.tile_size
                self.direction= (-1, 0)
            if keys[pygame.K_RIGHT]:
                new_position.x += 1 * self.tile_size
                self.direction = (1, 0)

            if self.direction:
                self.check_next_field(new_position)

        return self.position


    def check_next_field(self, new_position):
        grid_x = int((new_position.x - self.left_corner_x) / self.tile_size)
        grid_y = int((new_position.y - self.left_corner_y) / self.tile_size)

        field_type = self.level_board[grid_y][grid_x]

        if field_type == 0 or field_type == 3:
            self.move_player(new_position)
        elif field_type == 2:
            self.move_player_and_box(new_position)
        else:
            pass

    def move_player(self, new_position):
        self.position.update(new_position)

    def attempt_to_move_box(self, new_position):
        successfully_moved_box = False
        grid_x = int((new_position.x - self.left_corner_x) / self.tile_size)
        grid_y = int((new_position.y - self.left_corner_y) / self.tile_size)

        tile_behind_box_x = grid_x + self.direction[0]
        tile_behind_box_y = grid_y + self.direction[1]

        if self.level_board[tile_behind_box_y][tile_behind_box_x] != 1 and self.level_board[tile_behind_box_y][tile_behind_box_x] != 2:
            self.level_board[grid_y][grid_x] = 0
            self.level_board[tile_behind_box_y][tile_behind_box_x] = 2
            successfully_moved_box = True

        return successfully_moved_box

    def move_player_and_box(self, new_position):
        if self.attempt_to_move_box(new_position):
            self.move_player(new_position)
