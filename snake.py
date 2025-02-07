import sys,pygame,game_classes

# Core Elements and variables
pygame.init()

tile_size = 40
columns = 20
rows = 20
width, height = rows*tile_size, columns*tile_size
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()
game_active = True

font = pygame.font.Font(None, 50)

player = game_classes.Player(0, 0, tile_size, (255, 0, 0),width, height)
all_sprites = pygame.sprite.Group()
all_sprites.add(player)



while game_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
    screen.fill((0,0,0))

    keys = pygame.key.get_pressed()
    player.move(keys)
    player.collisions(width,height)
    screen.fill((0,0,0))
    if player.living == False:
        death_message = font.render("you died",True, 'white',None)
        death_message_rect = death_message.get_rect(topleft = (0,0))
        screen.blit(death_message, death_message_rect)

    for sprite in all_sprites:
        sprite.draw(screen)



    pygame.display.flip()
    clock.tick(60)
    



    