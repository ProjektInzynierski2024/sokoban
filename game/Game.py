import pygame

from common.Common import RGB_COLOR_BLACK
from common.Displayer import Displayer
from game.Player import Player

level = [
        [1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 3, 0, 0, 0, 0, 0, 3, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 0, 1, 2, 0, 2, 1, 0, 1],
        [1, 0, 0, 0, 0, 0, 0, 0, 1],
        [1, 0, 1, 2, 0, 2, 1, 0, 1],
        [1, 0, 1, 0, 0, 0, 1, 0, 1],
        [1, 3, 0, 0, 0, 0, 0, 3, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1]
    ]

class Game:
    def __init__(self, level_board):
        self.score = 0
        self.displayer = Displayer()
        self.left_corner_x, self.left_corner_y = self.displayer.get_left_corner_coordinates()
        self.tile_size = self.displayer.get_tile_size()
        self.level_board = level_board

    def check_boxes_on_targets(self):
        return not any(3 in row for row in self.level_board)

    def update_score(self):
        if self.check_boxes_on_targets():
            self.score += 100

    def run(self):
        running = True
        clock = pygame.time.Clock()
        initial_player_position = self.displayer.display_soldier_in_the_center()

        player = Player(
            start_position=initial_player_position,
            tile_size=self.tile_size,
            left_corner_x=self.left_corner_x,
            left_corner_y=self.left_corner_y,
            level_board=self.level_board
        )

        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False

            new_position = player.move()

            self.displayer.fill_display_with_color(color=RGB_COLOR_BLACK)
            self.displayer.display_level(level=self.level_board)
            self.displayer.display_soldier_on_position(soldier_position=new_position)
            self.update_score()
            self.displayer.display_score(score=self.score)
            self.displayer.flip()

            if self.score == 100:
                pygame.time.wait(2000)
                running = False

            clock.tick(8)
        pygame.quit()

if __name__ == "__main__":
    game = Game(level)
    game.run()

