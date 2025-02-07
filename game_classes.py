import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, size, color, screen_width, screen_height):
        super().__init__()
        self.rect = pygame.Rect(x, y, size, size)
        self.color = color
        self.velocity = size
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.is_on_ground = False
        self.direction = None
        self.living = True
        self.length = 2

    def move(self, keys):
    


        if self.living == True:
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.direction != "right":self.direction = "left"
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.direction != "left":self.direction = "right"
            elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.direction != "down":self.direction = "up"
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.direction != "up":self.direction = "down"
            
            if self.direction == 'left':
                self.rect.x -= self.velocity
                    
            elif self.direction == 'right':
                self.rect.x += self.velocity
            elif self.direction == 'up':
                self.rect.y -= self.velocity
 
            elif self.direction == 'down':
                self.rect.y += self.velocity


        

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)
    

    def collisions(self, width, height):
        if self.rect.left < 0:
            self.living = False
            self.direction=None
            self.rect.x += self.velocity
        elif self.rect.right > width: 
            self.living = False
            self.direction=None
            self.rect.x -= self.velocity
        elif self.rect.top < 0:
            self.living = False
            self.direction=None
            self.rect.y += self.velocity
        elif self.rect.bottom > height:
            self.living = False
            self.direction=None
            self.rect.y -= self.velocity
