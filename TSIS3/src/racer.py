import pygame
import time

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("../assets/player_car.png")
        self.shield_active = False
        self.nitro_end_time = 0

    def apply_powerup(self, p_type):
        if p_type == "Nitro":
            self.nitro_end_time = time.time() + 5 
        elif p_type == "Shield":
            self.shield_active = True
        elif p_type == "Repair":
           
            pass

    def is_nitro(self):
        return time.time() < self.nitro_end_time
