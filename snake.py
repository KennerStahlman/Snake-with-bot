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
    player = game_classes.Player(0, 0, tile_size, 'green', rows, columns)
    food = game_classes.Food(5,5,tile_size,'red', rows, columns)
    all_sprites = pygame.sprite.Group()
    all_sprites.add(food ,player)
    frame_count = 0  



FPS =500
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
    if player.living:
        if player.body[0] == food.position:
            while food.position in player.body:
                food.position = (random.randint(0, rows-1), random.randint(0,columns-1))
            player.grow_flag = True
        player.hamiltonian_cycle(columns, rows, food.position, len(player.body))
        # player.bfs(food.position)
        # player.better_greedy(food.position)
        # player.greedy_algo(food.position)
        # player.move(keys)
        player.collisions()
    screen.fill((0, 0, 0))

    keys = pygame.key.get_pressed()
    for sprite in all_sprites:
        sprite.draw(screen)
    score_message = font.render(f"score: {len(player.body)}", 0, 'red')
    screen.blit(score_message, (width - .3*(width),0))
    fps_message = font.render(f"mps: {round(clock.get_fps())}", True, 'red')
    screen.blit(fps_message, (10,10))
        
    if len(player.body) == rows * columns:
        death_message = font.render("You won, Press SPACE to restart", True, 'white')
        screen.blit(death_message, (0, rows*tile_size/2))

    elif not player.living:
        death_message = font.render("You died - Press SPACE to restart", True, 'white')
        screen.blit(death_message, (columns*tile_size/2, rows*tile_size/2))
    pygame.display.flip()
    clock.tick(FPS)