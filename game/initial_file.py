import pygame

from Board import Board

SCREEN_WIDTH = 900
SCREEN_HEIGHT = 900
TILE_SIZE = 90

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Sokoban")
clock = pygame.time.Clock()
dt = 0
wall_image = pygame.image.load('bricks.png').convert()
wall_image = pygame.transform.scale(wall_image, (TILE_SIZE, TILE_SIZE))
player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)


def draw_level(board):
    grid = board.grid
    rows = len(grid)
    columns = len(grid[0])

    offset_x = (SCREEN_WIDTH - columns * TILE_SIZE) // 2
    offset_y = (SCREEN_HEIGHT - rows * TILE_SIZE) // 2

    for y, row in enumerate(grid):
        for x, tile in enumerate(row):
            tile_value = tile.get_value()
            color = "gray"
            if tile_value == 1:
                color = "green"
                pygame.draw.rect(screen, color,
                                 (offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE))
            elif tile_value == 2:
                screen.blit(wall_image, (offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE))
            elif tile_value == 3:
                color = "blue"
                pygame.draw.rect(screen, color,
                                 (offset_x + x * TILE_SIZE, offset_y + y * TILE_SIZE, TILE_SIZE, TILE_SIZE))

def main():
    running = True

    #0 - movement area
    #1 - wall
    #2 - box
    #3 - place to put box

    board = Board(3)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((0, 0, 0))
        draw_level(board)
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
