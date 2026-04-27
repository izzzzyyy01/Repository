import pygame
import random

class Food:
    # Добавляем pos в аргументы
    def __init__(self, pos, color, points, weight=1, timer=None, food_type="normal"):
        self.pos = pos
        self.color = color
        self.points = points
        self.weight = weight 
        self.timer = timer  # Время в миллисекундах (например, 5000 для 5 сек)
        self.type = food_type
        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        if self.timer is None: return False
        return pygame.time.get_ticks() - self.spawn_time > self.timer

class Snake:
    def __init__(self, color):
       
        self.body = [[100, 60], [80, 60], [60, 60]]
        self.dir = "RIGHT"
        self.color = color
        self.shield = False 
        self.speed_modifier = 1.0 

    def move(self, step=20): 
        head = list(self.body[0])
        if self.dir == "UP": head[1] -= step
        if self.dir == "DOWN": head[1] += step
        if self.dir == "LEFT": head[0] -= step
        if self.dir == "RIGHT": head[0] += step
        
        self.body.insert(0, head)
        self.body.pop()

    def grow(self, n=1):
        for _ in range(n):
         
            self.body.append(list(self.body[-1]))

    def shrink(self, n=2):
        for _ in range(n):
            if len(self.body) > 0: 
                self.body.pop()
