def spawn_food(self, food_type="normal"):
        while True:
            x = random.randrange(0, self.width, self.cell_size)
            y = random.randrange(0, self.height, self.cell_size)
            pos = [x, y]
            
            
            if pos not in self.snake.body and pos not in self.obstacles:
                if food_type == "normal":
            
                    return Food(pos, (0, 255, 0), points=1, type="normal")
                elif food_type == "poison":
                    return Food(pos, (150, 0, 0), points=0, type="poison")
                break

    def generate_obstacles(self):
        self.obstacles = []
        num_blocks = self.level * 2
        for _ in range(num_blocks):
            while True:
                x = random.randrange(0, self.width, self.cell_size)
                y = random.randrange(0, self.height, self.cell_size)
                pos = [x, y]
                
               
                head_x, head_y = self.snake.body[0]
                if abs(x - head_x) > self.cell_size * 3 or abs(y - head_y) > self.cell_size * 3:
                    if pos not in self.snake.body:
                        self.obstacles.append(pos)
                        break

    def update(self):
        if self.game_over:
            return

        self.snake.move()
        head = self.snake.body[0]

    
        if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
            if self.snake.shield:
                self.snake.shield = False
                
                head[0] = max(0, min(head[0], self.width - self.cell_size))
                head[1] = max(0, min(head[1], self.height - self.cell_size))
            else:
                self.game_over = True

        
        if head in self.snake.body[1:] or head in self.obstacles:
            if self.snake.shield:
                self.snake.shield = False
               
            else:
                self.game_over = True

     
        for food in self.foods[:]:
            if head == food.pos:
                if food.type == "poison":
                    self.snake.body = self.snake.body[:-2] 
                    if len(self.snake.body) <= 1:
                        self.game_over = True
                else:
                    self.score += food.points
                    self.snake.grow() 
                
                self.foods.remove(food)
                self.check_level_up()
