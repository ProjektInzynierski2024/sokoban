import sys
import pygame
import subprocess
import os

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (232, 231, 227)
VIOLET = (236, 171, 167)

SCREEN_WIDTH = 700
SCREEN_HEIGHT = 700

FONT_SIZE = 40


class Menu:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Menu")
        self.font = pygame.font.Font(None, FONT_SIZE)
        self.assets_path = os.path.abspath("common/images")
        self.background = pygame.image.load(os.path.join(self.assets_path, "background.png"))

        self.options = [
            "PLAY THE GAME",
            "TRAIN THE AGENT"
        ]
        self.actions = [
            self.start_game,
            self.train_agent,
        ]
        self.selected_option = 0

    def draw_menu(self):

        self.screen.blit(pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT)), (0, 0))

        for i, option in enumerate(self.options):
            text_surface = self.font.render(option, True, WHITE)
            text_width = text_surface.get_width()
            text_height = text_surface.get_height()

            button_color = VIOLET if i == self.selected_option else GRAY
            button_width = text_width + 40
            button_height = text_height + 20
            button_rect = pygame.Rect((SCREEN_WIDTH // 2 - button_width // 2, SCREEN_HEIGHT // 2 - 100 + i * 80 + 50),
                                      (button_width, button_height))

            pygame.draw.rect(self.screen, button_color, button_rect, border_radius=10)
            pygame.draw.rect(self.screen, BLACK, button_rect, 4)

            text_rect = text_surface.get_rect(center=button_rect.center)
            self.screen.blit(text_surface, text_rect)

        pygame.display.flip()

    def start_game(self):
        subprocess.run([sys.executable, "game/Game.py"])

    def train_agent(self):
        subprocess.run([sys.executable, "model/Agent.py"])

    def run(self):
        while True:
            self.draw_menu()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_option = (self.selected_option - 1) % len(self.options)
                    elif event.key == pygame.K_DOWN:
                        self.selected_option = (self.selected_option + 1) % len(self.options)
                    elif event.key == pygame.K_RETURN:
                        self.actions[self.selected_option]()

if __name__ == "__main__":
    menu = Menu()
    menu.run()
