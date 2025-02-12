import pygame
from collections import deque

class Player(pygame.sprite.Sprite):
    def __init__(self, x, y, tile_size, color, grid_width, grid_height):
        super().__init__()
        self.tile_size = tile_size
        self.grid_width = grid_width
        self.grid_height = grid_height
        self.color = color
        
        # Use grid positions (0-19) instead of pixels
        self.body = [(x, y)]
        self.direction = "right"
        self.living = True
        self.grow_flag = False  # Controls whether the snake should grow

    def hamiltonian_cycle(self, width, height, foodposition, score):
        head_x, head_y = self.body[0]
        if len(self.body) > width * height /2.5 or foodposition[1] == 0:
            if width % 2 == 0:
                if head_x % 2 == 0 and (head_y != 0 or head_x == 0):
                    self.direction = "down"
                if head_y == height-1:
                    self.direction = "right"
                if head_x % 2 != 0 :
                    self.direction = "up"
                if head_y == 1 and head_x != 0 and head_x != width-1 and head_x % 2 != 0:
                    self.direction = "right"
                if head_y == 0 and head_x != 0:
                    self.direction = "left"
        elif foodposition[1] != 0 and foodposition[1] not in [i for i in range(height) if i > height/2]:
            if width % 2 == 0:
                if head_x % 2 == 0 and (head_y != 0 or head_x == 0):
                    self.direction = "down"
                if head_y > foodposition[1]+height/2.4:
                    self.direction = "right"
                if head_x % 2 != 0 :
                    self.direction = "up"
                if head_y <= foodposition[1] and head_x != 0 and head_x != width-1 and head_x % 2 != 0:
                    self.direction = "right"
                if head_y == 0 and head_x != 0:
                    self.direction = "left"

        else:
            if width % 2 == 0:
                if head_x % 2 == 0 and (head_y != 0 or head_x == 0):
                    self.direction = "down"
                if head_y >= foodposition[1]:
                    self.direction = "right"
                if head_x % 2 != 0 :
                    self.direction = "up"
                if head_y <= foodposition[1] - height/2.4  and head_x != 0 and head_x != width-1 and head_x % 2 != 0:
                    self.direction = "right"
                if head_y == 0 and head_x != 0:
                    self.direction = "left"
        
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

                if (0 <= nx < self.grid_width and 0 <= ny < self.grid_height and
                    (nx, ny) not in set(self.body) and (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited.add((nx, ny))

        return count

    def path_to_food(self, start_pos, food_position):
        """Checks if the snake can still reach the food from start_pos."""
        queue = deque([start_pos])
        visited = set()
        visited.add(start_pos)

        tail = self.body[-1]  # Allow movement into the last tail position

        while queue:
            x, y = queue.popleft()
            if (x, y) == food_position:
                return True

            for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nx, ny = x + dx, y + dy

                if (0 <= nx < self.grid_width and 0 <= ny < self.grid_height and
                    ((nx, ny) not in set(self.body) or (nx, ny) == tail) and
                    (nx, ny) not in visited):
                    queue.append((nx, ny))
                    visited.add((nx, ny))

        return False  # No path found to the food

    def bfs(self, food_position):
        """Determines the best move using BFS-based logic with flood fill and path checking."""
        if not self.living:
            return

        head_x, head_y = self.body[0]
        body_positions = set(self.body[1:])  # Keep entire body except head

        # Define possible moves
        moves = {
            "left":  (head_x - 1, head_y),
            "right": (head_x + 1, head_y),
            "up":    (head_x, head_y - 1),
            "down":  (head_x, head_y + 1)
        }

        # Compute valid moves
        valid_moves = {dir: pos for dir, pos in moves.items()
                       if pos not in body_positions and 0 <= pos[0] < self.grid_width and 0 <= pos[1] < self.grid_height}
        
        if not valid_moves:
            self.living = False
            return  # Snake stops moving and dies

        if not valid_moves:
            return  # Do nothing if no valid moves exist

        # 1️⃣ Compute flood fill for each valid move
        best_move = None
        max_space = -1

        for direction, position in valid_moves.items():
            open_space = self.flood_fill(position)

            # Check if this move keeps the path to food open
            if open_space > max_space and self.path_to_food(position, food_position):  
                max_space = open_space
                best_move = direction  # Choose move with max open space that still allows a path to food

        # 2️⃣ Try greedy move first if it's safe
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
                self.direction = best_move  # Flood fill is better
            elif future_space > len(self.body) * 1.5 and self.path_to_food(valid_moves[greedy_move], food_position):
                self.direction = greedy_move  # Greedy move is safe
            else:
                self.direction = best_move if best_move else max(valid_moves, key=lambda d: self.flood_fill(valid_moves[d]))


        elif best_move:
            self.direction = best_move


        elif valid_moves:
            self.direction = max(valid_moves, key=lambda d: self.flood_fill(valid_moves[d]))  # Pick the safest move

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
                head_x, head_y = self.body[0]  # Get the head position

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


    def move(self, keys):
        if self.living:
            if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and self.direction != "right":
                self.direction = "left"
            elif (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and self.direction != "left":
                self.direction = "right"
            elif (keys[pygame.K_UP] or keys[pygame.K_w]) and self.direction != "down":
                self.direction = "up"
            elif (keys[pygame.K_DOWN] or keys[pygame.K_s]) and self.direction != "up":
                self.direction = "down"
            

            # if self.direction:
            #     head_x, head_y = self.body[0]  # Get the head position

            #     if self.direction == 'left':
            #         head_x -= 1
            #     elif self.direction == 'right':
            #         head_x += 1
            #     elif self.direction == 'up':
            #         head_y -= 1
            #     elif self.direction == 'down':
            #         head_y += 1


            #     self.body.insert(0, (head_x, head_y))


            #     if not self.grow_flag:
            #         self.body.pop()
            #     else:
            #         self.grow_flag = False

    def draw(self, screen):

        for segment in self.body:
            x, y = segment[0] * self.tile_size, segment[1] * self.tile_size
            pygame.draw.rect(screen, self.color, (x, y, self.tile_size, self.tile_size))

    def collisions(self):
        head_x, head_y = self.body[0]


        if head_x < 0 or head_x >= self.grid_width or head_y < 0 or head_y >= self.grid_height:
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
        

        self.position = (x, y) 


    def draw(self, screen):
        x, y = self.position[0] * self.tile_size, self.position[1] * self.tile_size
        pygame.draw.rect(screen, self.color, (x, y, self.tile_size, self.tile_size))