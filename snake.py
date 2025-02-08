import sys
import pygame
import game_classes
import random

pygame.init()

tile_size = 30
columns = 20
rows = 20
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
    frame_count = 0  



FPS = 60
MOVE_DELAY = 1
frame_count = 0


reset_game()

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE and not player.living:
            reset_game()

    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()

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



    for sprite in all_sprites:
        sprite.draw(screen)

    if not player.living:
        death_message = font.render("You died - Press SPACE to restart", True, 'white')
        screen.blit(death_message, (10, 10))

    pygame.display.flip()
    clock.tick(FPS)
    frame_count += 1