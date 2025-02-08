import sys
import pygame
import game_classes
import random

# Core Elements and variables
pygame.init()

tile_size = 30
columns = 40
rows = 40
width, height = rows * tile_size, columns * tile_size
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
game_active = True

font = pygame.font.Font(None, 50)

def reset_game():
    """Resets the game variables and restarts the game."""
    global player, food,all_sprites, frame_count
    player = game_classes.Player(5, 10, tile_size, 'green', rows, columns)
    food = game_classes.Food(9,9,tile_size,'red', rows, columns)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(food ,player)
    frame_count = 0  # Reset frame counter


# Movement control variables
FPS = 60
MOVE_DELAY = 1  # Move every 6 frames (~10 moves per second at 60 FPS)
frame_count = 0  # Keeps track of frames

# Initialize the first game instance
reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        # Restart the game if SPACE is pressed after dying
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not player.living:
            reset_game()

    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()

    # Only move the snake every MOVE_DELAY frames
    if player.living:
        if player.body[0] == food.position:
            while food.position in player.body:
                food.position = (random.randint(0, rows-1), random.randint(0,columns-1))
            player.grow_flag = True

        player.bfs(food.position)
        # player.better_greedy(food.position)
        # player.greedy_algo(food.position)
        # player.move(keys)
        player.collisions()


    if not player.living:
        death_message = font.render("You died - Press SPACE to restart", True, 'white')
        screen.blit(death_message, (10, 10))

    for sprite in all_sprites:
        sprite.draw(screen)

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1