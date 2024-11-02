import pygame

from generator.initial_file import generate_level

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
TILE_SIZE = 40

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban")
clock = pygame.time.Clock()
dt = 0

player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


def draw_level(level):
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            if tile == 1:
                pygame.draw.rect(screen, "green", (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile == 2:
                pygame.draw.rect(screen, "red", (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            if tile == 3:
                pygame.draw.rect(screen, "blue", (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(screen, "gray", (x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def main():
    running = True

    #0 - movement area
    #1 - wall
    #2 - box
    #3 - place to put box


    level = [[1,2,0,1],
             [0,0,0,0],
             [1,1,3,1]]

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_level(level)
        pygame.display.flip()

    pygame.draw.circle(screen, "pink", player_pos, 40)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        player_pos.y -= 300 * dt
    if keys[pygame.K_s]:
        player_pos.y += 300 * dt
    if keys[pygame.K_a]:
        player_pos.x -= 300 * dt
    if keys[pygame.K_d]:
        player_pos.x += 300 * dt

    pygame.quit()

if __name__ == "__main__":
    main()
