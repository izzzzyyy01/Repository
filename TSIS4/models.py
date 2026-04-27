import pygame
import random

class Food:
    def __init__(self, color, points, weight=1, timer=None):
        self.pos = [0, 0]
        self.color = color
        self.points = points
        self.weight = weight 
        self.timer = timer  
        self.spawn_time = pygame.time.get_ticks()

    def is_expired(self):
        if self.timer is None: return False
        return pygame.time.get_ticks() - self.spawn_time > self.timer

class Snake:
    def __init__(self, color):
        self.body = [[100, 50], [90, 50], [80, 50]]
        self.dir = "RIGHT"
        self.color = color
        self.shield = False 

    def move(self):
        head = list(self.body[0])
        if self.dir == "UP": head[1] -= 10
        if self.dir == "DOWN": head[1] += 10
        if self.dir == "LEFT": head[0] -= 10
        if self.dir == "RIGHT": head[0] += 10
        self.body.insert(0, head)
        self.body.pop()

    def grow(self, n=1):
        for _ in range(n):
            self.body.append(list(self.body[-1]))

    def shrink(self, n=2):
        for _ in range(n):
            if len(self.body) > 1:
                self.body.pop()
