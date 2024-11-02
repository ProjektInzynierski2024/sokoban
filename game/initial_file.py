import pygame

TITLE_BAR_SIZE_IN_PIXELS = 60
TILES_PER_ROW = 9

def initialize_pygame_display():
    pygame.init()
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h - TITLE_BAR_SIZE_IN_PIXELS
    pygame.display.set_caption("Sokoban")
    return pygame.display.set_mode((width, height), pygame.RESIZABLE),  width, height


display, display_width, display_height = initialize_pygame_display()

calculate_tile_size = min(
    display_width // TILES_PER_ROW,
    (display_height - 100) // TILES_PER_ROW
)

TILE_SIZE = calculate_tile_size
tile_grid_width = TILES_PER_ROW * TILE_SIZE
tile_grid_height = TILES_PER_ROW * TILE_SIZE

left_corner_x_coordinate = (display_width - tile_grid_width) // 2
left_corner_y_coordinate = (display_height - tile_grid_height) // 2

def draw_level(level):
    for y, row in enumerate(level):
        for x, tile in enumerate(row):
            tile_x_coordinate = left_corner_x_coordinate + x * TILE_SIZE
            tile_y_coordinate = left_corner_y_coordinate + y * TILE_SIZE

            if tile == 1:
                pygame.draw.rect(display, "green", (tile_x_coordinate, tile_y_coordinate, TILE_SIZE, TILE_SIZE))
            elif tile == 2:
                pygame.draw.rect(display, "red", (tile_x_coordinate, tile_y_coordinate, TILE_SIZE, TILE_SIZE))
            elif tile == 3:
                pygame.draw.rect(display, "blue", (tile_x_coordinate, tile_y_coordinate, TILE_SIZE, TILE_SIZE))
            else:
                pygame.draw.rect(display, "gray", (tile_x_coordinate, tile_y_coordinate, TILE_SIZE, TILE_SIZE))


level = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 2, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 3, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def is_collision(new_position):
    grid_x = int((new_position.x - left_corner_x_coordinate) / TILE_SIZE)
    grid_y = int((new_position.y - left_corner_y_coordinate) / TILE_SIZE)

    return level[grid_y][grid_x] == 1


def main():
    running = True
    clock = pygame.time.Clock()
    player_position = pygame.Vector2(display.get_width() / 2, display.get_height() / 2)

    while running:
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        new_position = player_position.copy()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            new_position.y -= 300 * delta_time
        if keys[pygame.K_s]:
            new_position.y += 300 * delta_time
        if keys[pygame.K_a]:
            new_position.x -= 300 * delta_time
        if keys[pygame.K_d]:
            new_position.x += 300 * delta_time

        if not is_collision(new_position):
            player_position = new_position

        display.fill((0, 0, 0))
        draw_level(level)

        pygame.draw.circle(display, "pink", player_position, 40)
        pygame.display.flip()

    pygame.quit()

if __name__ == "__main__":
    main()
