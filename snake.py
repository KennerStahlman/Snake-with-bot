import sys
import pygame
import game_classes
import random


pygame.init()

tile_size = 50
columns = 10
rows = 10
width, height = rows * tile_size, columns * tile_size
screen = pygame.display.set_mode((width+tile_size*4, height+tile_size*4))
clock = pygame.time.Clock()
game_active = True
obs_on = True

class Board(pygame.sprite.Sprite):
    def __init__(self,):
        super().__init__()
        self.board = [(j,i) for i in range(rows) for j in range(columns)]
        self.darktiles = [i for i in self.board if (i[0]+i[1]+2)%2 != 0]
        self.lighttiles = [i for i in self.board if (i[0]+i[1]+2)%2 == 0 ]
        self.darktiles_rect = [pygame.Rect(i[0]*tile_size+100, i[1]*tile_size+100, tile_size, tile_size) for i in self.darktiles]
        self.lighttiles_rect = [pygame.Rect(i[0]*tile_size+100, i[1]*tile_size+100, tile_size, tile_size) for i in self.lighttiles]
    def draw(self,screen):  
        [pygame.draw.rect(screen, 'light grey', self.darktiles_rect[i]) for i in range(columns*rows//2)]
        [pygame.draw.rect(screen, 'dark grey', self.lighttiles_rect[i]) for i in range(columns*rows//2)]

font = pygame.font.Font(None, 50)

def reset_game():
    """Resets the game variables and restarts the game."""
    global player, food, all_sprites, frame_count, board, obstacles
    

    board = Board()
    player = game_classes.Player(2, 5, tile_size, 'green', rows, columns)
    food = game_classes.Food(8, 5, tile_size, 'red', rows, columns)
    
    if obs_on:
        reserved_positions = [(2+2, 5+2), (1+2, 5+2), (3+2, 5+2), (8+2, 5+2)]

        obs_count = random.randint(1, 5)
        obstacles = []
        
        while len(obstacles) < obs_count:

            width = random.randint(1, 3)
            height = random.randint(1, 3)
            x = random.randint(0, 9)
            y = random.randint(0, 9)

            if x + width > 9 or y + height > 9:
                continue
                
            new_obstacle = game_classes.Obstacle(width, height, x, y, 'orange', tile_size)

            collision = False
            for pos in reserved_positions:
                if pygame.Rect.collidepoint(new_obstacle.rect, pos[0]*tile_size, pos[1]*tile_size):
                    collision = True
                    break

            for existing_obs in obstacles:
                if pygame.Rect.colliderect(new_obstacle.rect, existing_obs.rect):
                    collision = True
                    break
                    
            if not collision:
                obstacles.append(new_obstacle)
    else:
        obstacles = []

    all_sprites = pygame.sprite.Group()
    all_sprites.add(board, food, player, *obstacles)
    frame_count = 0



FPS = 10
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
    keys = pygame.key.get_pressed()

    player.collisions(obstacles)

    if player.living and frame_count%MOVE_DELAY == 0:
        if player.body[0] == food.position:
            while food.position in player.body:
                food.position = (random.randint(2, rows+1), random.randint(2,columns+1))
                for obstacle in obstacles:
                    while pygame.Rect.collidepoint(obstacle.rect, food.position[0]*tile_size, food.position[1]*tile_size):
                        food.position = (random.randint(2, rows+1), random.randint(2,columns+1))
            player.grow_flag = True
        # player.follow_hamiltonian_cycle(rows, columns, obstacles)
        # player.bfs(food.position)
        # player.greedy_algo(food.position)
        player.move(keys,obstacles)
    screen.fill((0, 0, 0))

    for sprite in all_sprites:
        sprite.draw(screen)
    score_message = font.render(f"score: {len(player.body)}", 0, 'red')
    score_rect = score_message.get_rect(topleft=(width//2+25, 50))
    screen.blit(score_message, score_rect)
    fps_message = font.render(f"mps: {round(clock.get_fps())}", True, 'red')
    screen.blit(fps_message, (10,10))
        
    if len(player.body) == rows * columns:
        death_message = font.render("You won, Press SPACE to restart", True, 'white')
        screen.blit(death_message, (0, rows*tile_size/2))
        player.living = False

    elif not player.living:
        death_message = font.render("You died - Press SPACE to restart", True, 'white')
        screen.blit(death_message, (columns*tile_size/2, rows*tile_size/2))
    frame_count+=1
    pygame.display.flip()
    clock.tick(FPS)