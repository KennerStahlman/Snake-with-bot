import pygame
from collections import deque


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, width, height, x ,y, color, tile_size):
        super().__init__()
        self.tile_size = tile_size
        self.color = color
        self.rect = pygame.Rect((x+2)*tile_size, (y+2)*tile_size, width*tile_size, height*tile_size)
    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.rect)

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, color, grid_width, grid_height):
        super().__init__()
        self.tile_size = tile_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.color = color
        
        self.body = [(x+2, y+2), (x+1, y+2)]
        self.direction = "right"
        self.living = True
        self.grow_flag = False 
        self.hamiltonian_cycle = None  # Store the cycle
        self.current_cycle_index = 0 
        self.generate_hamiltonian_cycle()  # Generate cycle on initialization

    def generate_hamiltonian_cycle(self):
        x_start = 2
        y_start = 2
        x_end = x_start + self.grid_width -1
        y_end = y_start + self.grid_height -1
        

        next_pos = {}
        

        if self.grid_width % 2 == 0:
            for y in range(y_start, y_end + 1):
                if (y - y_start) % 2 == 0:
                    for x in range(x_start, x_end):
                        next_pos[(x, y)] = (x + 1, y)
                    next_pos[(x_end, y)] = (x_end, y + 1)
                else:
                    for x in range(x_end, x_start, -1):
                        next_pos[(x, y)] = (x - 1, y)
                    next_pos[(x_start, y)] = (x_start, y + 1)
            
            for y in range(y_end, y_start, -1):
                next_pos[(x_end, y)] = (x_end, y - 1)
            
            next_pos[(x_end, y_start)] = (x_start, y_start)
        
        elif self.grid_height % 2 == 0:
            for x in range(x_start, x_end + 1):
                if (x - x_start) % 2 == 0:
                    for y in range(y_start, y_end):
                        next_pos[(x, y)] = (x, y + 1)
                    next_pos[(x, y_end)] = (x + 1, y_end)
                else:
                    for y in range(y_end, y_start, -1):
                        next_pos[(x, y)] = (x, y - 1)
                    next_pos[(x, y_start)] = (x + 1, y_start)
            
            for x in range(x_end, x_start, -1):
                next_pos[(x, y_end)] = (x - 1, y_end)
            
            next_pos[(x_start, y_end)] = (x_start, y_start)
        
        self.hamiltonian_cycle = next_pos

    def follow_hamiltonian_cycle(self, width, height, obstacles):
        """Use the Hamiltonian cycle to determine next move."""
        head_x, head_y = self.body[0]
        
        rel_x = head_x - 2
        rel_y = head_y - 2
        
        width = width
        height = height
        print(self.body[0])
        print(self.hamiltonian_cycle[self.body[0]])
        if self.body[0][0] > self.hamiltonian_cycle[self.body[0]][0]:
            self.direction == 'left'
        if self.body[0][0] < self.hamiltonian_cycle[self.body[0]][0]:
            self.direction == 'right'
        if self.body[0][1] > self.hamiltonian_cycle[self.body[0]][1]:
            self.direction == 'up'
        if self.body[0][1] < self.hamiltonian_cycle[self.body[0]][1]:
            self.direction == 'down'
        if self.direction:
            if self.direction == 'left':
                head_x -= 1
            elif self.direction == 'right':
                head_x += 1
            elif self.direction == 'up':
                head_y -= 1
            elif self.direction == 'down':
                head_y += 1

            self.body.insert(0, (head_x, head_y))
            self.collisions(obstacles)
            if self.living == False:
                self.body.remove((head_x, head_y))
            elif not self.grow_flag:
                self.body.pop()
            else:
                self.grow_flag = False

    def flood_fill(self, start_pos):
        """Returns the number of open spaces reachable from start_pos."""
        queue = deque([start_pos])
        visited = set()
        visited.add(start_pos)
        count = 0
        
        while queue:
            x, y = queue.popleft()
            count += 1

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy

                if (1 < nx < self.grid_width+2 and 1 < ny < self.grid_height+2 and
                    (nx, ny) not in set(self.body) and (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited.add((nx, ny))

        return count

    def path_to_food(self, start_pos, food_position):
        """Checks if the snake can still reach the food from start_pos."""
        queue = deque([start_pos])
        visited = set()
        visited.add(start_pos)

        tail = self.body[-1]

        while queue:
            x, y = queue.popleft()
            if (x, y) == food_position:
                return True

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy

                if (1 < nx < self.grid_width+2 and 1 < ny < self.grid_height+2 and
                    ((nx, ny) not in set(self.body) or (nx, ny) == tail) and
                    (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited.add((nx, ny))

        return False

    def bfs(self, food_position):
        """Determines the best move using BFS-based logic with flood fill and path checking."""
        if not self.living:
            return

        head_x, head_y = self.body[0]
        body_positions = set(self.body[1:])

        moves = {
            "left":  (head_x - 1, head_y),
            "right": (head_x + 1, head_y),
            "up":    (head_x, head_y - 1),
            "down":  (head_x, head_y + 1)
        }

        valid_moves = {dir: pos for dir, pos in moves.items()
                       if pos not in body_positions and 1 < pos[0] < self.grid_width+2 and 1 < pos[1] < self.grid_height+2}
        
        if not valid_moves:
            self.living = False
            return

        if not valid_moves:
            return 
        best_move = None
        max_space = -1

        for direction, position in valid_moves.items():
            open_space = self.flood_fill(position)


            if open_space > max_space and self.path_to_food(position, food_position):  
                max_space = open_space
                best_move = direction 

        greedy_move = None
        if head_x > food_position[0] and "left" in valid_moves:
            greedy_move = "left"
        elif head_x < food_position[0] and "right" in valid_moves:
            greedy_move = "right"
        elif head_y > food_position[1] and "up" in valid_moves:
            greedy_move = "up"
        elif head_y < food_position[1] and "down" in valid_moves:
            greedy_move = "down"


        if greedy_move and greedy_move in valid_moves:
            future_space = self.flood_fill(valid_moves[greedy_move])
            if best_move and future_space < max_space:
                self.direction = best_move
            elif future_space > len(self.body) * 1.5 and self.path_to_food(valid_moves[greedy_move], food_position):
                self.direction = greedy_move
            else:
                self.direction = best_move if best_move else max(valid_moves, key=lambda d: self.flood_fill(valid_moves[d]))


        elif best_move:
            self.direction = best_move


        elif valid_moves:
            self.direction = max(valid_moves, key=lambda d: self.flood_fill(valid_moves[d]))

        if not self.direction:
            self.living = False
            return


        if self.direction:
            if self.direction == 'left':
                head_x -= 1
            elif self.direction == 'right':
                head_x += 1
            elif self.direction == 'up':
                head_y -= 1
            elif self.direction == 'down':
                head_y += 1


            self.body.insert(0, (head_x, head_y))


            if not self.grow_flag:
                self.body.pop()
            else:
                self.grow_flag = False  

    def better_greedy(self, food_position):
        if self.living:
            
            head_x, head_y = self.body[0]

            body_positions = set(self.body[1:])

            moves = {
                "left":  (head_x - 1, head_y),
                "right": (head_x + 1, head_y),
                "up":    (head_x, head_y - 1),
                "down":  (head_x, head_y + 1)
            }

            valid_moves = {dir for dir, pos in moves.items() if pos not in body_positions and 0 <= pos[0] < self.grid_width and 0<= pos[1] < self.grid_height}
            print(valid_moves)
            
            if self.body[0][0] > food_position[0] and "left" in valid_moves:
                self.direction = "left"
            elif self.body[0][0] < food_position[0] and "right" in valid_moves:
                self.direction = "right"
            elif self.body[0][1] > food_position[1] and "up" in valid_moves:
                self.direction = "up"
            elif self.body[0][1] < food_position[1] and "down" in valid_moves:
                self.direction = "down"
            
            if self.direction not in valid_moves and valid_moves:
                self.direction = next(iter(valid_moves))
            if self.direction:

                if self.direction == 'left':
                    head_x -= 1
                elif self.direction == 'right':
                    head_x += 1
                elif self.direction == 'up':
                    head_y -= 1
                elif self.direction == 'down':
                    head_y += 1

                self.body.insert(0, (head_x, head_y))

                if not self.grow_flag:
                    self.body.pop() 
                else:
                    self.grow_flag = False  

    def greedy_algo(self, food_position):
        if self.living:
            if self.body[0][0] > food_position[0] and self.direction != "right" :
                self.direction = "left"
            if self.body[0][0] < food_position[0] and self.direction != "left":
                self.direction = "right"
            if self.body[0][1] > food_position[1] and self.direction != "down":
                self.direction = "up"
            if self.body[0][1] < food_position[1] and self.direction != "up":
                self.direction = "down"
            
            if self.direction:
                head_x, head_y = self.body[0]

                if self.direction == 'left':
                    head_x -= 1
                elif self.direction == 'right':
                    head_x += 1
                elif self.direction == 'up':
                    head_y -= 1
                elif self.direction == 'down':
                    head_y += 1

                self.body.insert(0, (head_x, head_y))

                if not self.grow_flag:
                    self.body.pop()  
                else:
                    self.grow_flag = False 


    def move(self, keys,obstacles):
        self.collisions(obstacles)
        if self.living:
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.direction != "right":
                self.direction = "left"
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.direction != "left":
                self.direction = "right"
            elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.direction != "down":
                self.direction = "up"
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.direction != "up":
                self.direction = "down"


            if self.direction:
                head_x, head_y = self.body[0]

                if self.direction == 'left':
                    head_x -= 1
                elif self.direction == 'right':
                    head_x += 1
                elif self.direction == 'up':
                    head_y -= 1
                elif self.direction == 'down':
                    head_y += 1

                self.body.insert(0, (head_x, head_y))
                self.collisions(obstacles)
                if not self.living:
                    self.body.remove((head_x, head_y))
                if not self.grow_flag:
                    self.body.pop()
                else:
                    self.grow_flag = False

    def draw(self, screen):

        for segment in self.body:
            x, y = segment[0] * self.tile_size, segment[1] * self.tile_size
            pygame.draw.rect(screen, self.color, (x, y, self.tile_size, self.tile_size))

    def collisions(self, obstacles):
        head_x, head_y = self.body[0]
        for obstacle in obstacles:
            if pygame.Rect.collidepoint(obstacle.rect, head_x*self.tile_size, head_y*self.tile_size):
                self.living = False

        if head_x < 2 or head_x > self.grid_width+1 or head_y < 2 or head_y > self.grid_height+1:
            self.living = False


        if (head_x, head_y) in self.body[1:]:
            self.living = False

    def grow(self):
        """Trigger snake growth on food consumption"""
        self.grow_flag = True

class Food(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, color, grid_width, grid_height):
        super().__init__()
        self.tile_size = tile_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.color = color
        

        self.position = (x+2, y+2) 


    def draw(self, screen):
        x, y = self.position[0] * self.tile_size, self.position[1] * self.tile_size
        pygame.draw.rect(screen, self.color, (x, y, self.tile_size, self.tile_size))

