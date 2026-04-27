import pygame
import random
from models import Snake, Food

class GameLogic:
    def __init__(self, settings):
        self.settings = settings
        self.width = settings['screen_width']
        self.height = settings['screen_height']
        self.cell_size = 20 
        
        self.snake = Snake(settings['snake_color'])
        self.foods = []
        self.obstacles = []
        
        self.score = 0
        self.level = 1
        self.game_over = False
        
     
        self.powerup_active = None
        self.powerup_end_time = 0

    def spawn_food(self, food_type="normal"):
        """Генерирует еду, избегая змею и препятствия"""
        while True:
            x = random.randrange(0, self.width, self.cell_size)
            y = random.randrange(0, self.height, self.cell_size)
            pos = [x, y]
            
            if pos not in self.snake.body and pos not in self.obstacles:
                if food_type == "normal":
                    return Food((0, 255, 0), points=1, weight=1)
                elif food_type == "poison":
                    return Food((150, 0, 0), points=0, weight=0) 
           
                break

    def check_level_up(self):
        """Повышение уровня каждые 5 очков"""
        new_level = (self.score // 5) + 1
        if new_level > self.level:
            self.level = new_level
            if self.level >= 3:
                self.generate_obstacles()

    def generate_obstacles(self):
        """Создает случайные стены, не задевая голову змеи"""
        self.obstacles = []
        num_blocks = self.level * 2
        for _ in range(num_blocks):
            while True:
                x = random.randrange(0, self.width, self.cell_size)
                y = random.randrange(0, self.height, self.cell_size)
                
                if abs(x - self.snake.body[0][0]) > self.cell_size * 3:
                    self.obstacles.append([x, y])
                    break

    def update(self):
        """Основная итерация логики"""
        if self.game_over:
            return

        self.snake.move()
        head = self.snake.body[0]

 
        if head[0] < 0 or head[0] >= self.width or head[1] < 0 or head[1] >= self.height:
            if self.snake.shield: 
                self.snake.shield = False
            else:
                self.game_over = True

    
        if head in self.snake.body[1:] or head in self.obstacles:
            self.game_over = True

       
