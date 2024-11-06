import pygame

TITLE_BAR_SIZE_IN_PIXELS = 60
TILES_PER_ROW = 9

score = 0

def initialize_pygame_display():
    pygame.init()
    info = pygame.display.Info()
    width, height = info.current_w, info.current_h - TITLE_BAR_SIZE_IN_PIXELS
    pygame.display.set_caption("Sokoban")
    font = pygame.font.Font(None, 36)
    return pygame.display.set_mode((width, height), pygame.RESIZABLE),  width, height, font


display, display_width, display_height, display_font = initialize_pygame_display()

calculate_tile_size = min(
    display_width // TILES_PER_ROW,
    (display_height - 100) // TILES_PER_ROW
)

TILE_SIZE = calculate_tile_size
tile_grid_width = TILES_PER_ROW * TILE_SIZE
tile_grid_height = TILES_PER_ROW * TILE_SIZE

left_corner_x_coordinate = (display_width - tile_grid_width) // 2
left_corner_y_coordinate = (display_height - tile_grid_height) // 2

def draw_level():
    score_text = display_font.render(f"Score: {score}", True, (255, 255, 255))
    display.blit(score_text, (10, 10))

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

#0 - movement area
#1 - wall
#2 - box
#3 - place to put box (target)
level = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 3, 0, 0, 0, 0, 0, 3, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 0, 2, 0, 2, 0, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 3, 0, 0, 0, 0, 0, 3, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1]
]

def check_next_field(new_position, player_position, direction):
    grid_x = int((new_position.x - left_corner_x_coordinate) / TILE_SIZE)
    grid_y = int((new_position.y - left_corner_y_coordinate) / TILE_SIZE)

    field_type = level[grid_y][grid_x]

    if field_type == 0:
        move_player(new_position, player_position)
    elif field_type == 2:
        move_player_and_box(direction, new_position, player_position)
    else:
        pass

def move_player(new_position, player_position):
    player_position.update(new_position)

def attempt_to_move_box(new_position, direction):
    successfully_moved_box = False
    grid_x = int((new_position.x - left_corner_x_coordinate) / TILE_SIZE)
    grid_y = int((new_position.y - left_corner_y_coordinate) / TILE_SIZE)

    tile_behind_box_x = grid_x + direction[0]
    tile_behind_box_y = grid_y + direction[1]

    if level[tile_behind_box_y][tile_behind_box_x] != 1 and level[tile_behind_box_y][tile_behind_box_x] != 2:
        level[grid_y][grid_x] = 0
        level[tile_behind_box_y][tile_behind_box_x] = 2
        successfully_moved_box = True

    return successfully_moved_box

def move_player_and_box(direction, new_position, player_position):
    if attempt_to_move_box(new_position, direction):
        move_player(new_position, player_position)
        update_score()

def check_boxes_on_targets():
    return not any(3 in row for row in level)

def update_score():
    global score
    if check_boxes_on_targets():
        score += 100


def main():
    running = True
    clock = pygame.time.Clock()
    player_position = pygame.Vector2(display.get_width() / 2, display.get_height() / 2)

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        new_position = player_position.copy()

        direction = None
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            new_position.y -= 1 * TILE_SIZE
            direction = (0,-1)
        if keys[pygame.K_s]:
            new_position.y += 1 * TILE_SIZE
            direction = (0, 1)
        if keys[pygame.K_a]:
            new_position.x -= 1 * TILE_SIZE
            direction = (-1, 0)
        if keys[pygame.K_d]:
            new_position.x += 1 * TILE_SIZE
            direction = (1, 0)

        if direction:
            check_next_field(new_position, player_position, direction)

        display.fill((0, 0, 0))
        draw_level()

        pygame.draw.circle(display, "pink", player_position, 40)
        pygame.display.flip()
        clock.tick(8)

    pygame.quit()

if __name__ == "__main__":
    main()
