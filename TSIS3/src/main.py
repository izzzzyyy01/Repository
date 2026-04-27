import pygame
import random
import time
from persistence import load_json, add_to_leaderboard
from ui import get_user_name, draw_button


pygame.init()
WIDTH, HEIGHT = 400, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Racer Advanced")
clock = pygame.time.Clock()


WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
settings = load_json("../settings.json", {"difficulty": 5, "speed": 5})

# Класс игрока
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(center=(WIDTH // 2, HEIGHT - 70))
        self.speed = 5
        self.shield_active = False
        self.nitro_boost = 1

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and self.rect.left > 0: self.rect.x -= self.speed * self.nitro_boost
        if keys[pygame.K_RIGHT] and self.rect.right < WIDTH: self.rect.x += self.speed * self.nitro_boost

# Класс врага
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((40, 60))
        self.image.fill((255, 0, 0)) 
        self.rect = self.image.get_rect(center=(random.randint(40, WIDTH-40), -100))
        self.speed = settings["difficulty"]

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.center = (random.randint(40, WIDTH-40), -100)


player = Player()
enemies = pygame.sprite.Group()
enemies.add(Enemy())
all_sprites = pygame.sprite.Group(player, *enemies)


state = "MENU"
user_name = "Guest"
score = 0
distance = 0
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        if state == "MENU":
            if event.type == pygame.MOUSEBUTTONDOWN:
               
                user_name = get_user_name(screen)
                state = "GAME"

    if state == "GAME":

        all_sprites.update()
        distance += 0.1
        score += 1 

       
        for enemy in enemies:
            if pygame.sprite.collide_rect(player, enemy):
                if player.shield_active:
                    player.shield_active = False  
                    enemy.rect.top = -100         
                else:
                    
                    add_to_leaderboard(user_name, int(score), int(distance))
                    state = "GAMEOVER"
       

        screen.fill(BLACK)
        all_sprites.draw(screen)

        
        font = pygame.font.SysFont("Arial", 20)
        score_txt = font.render(f"Score: {int(score)}  Dist: {int(distance)}", True, WHITE)
        screen.blit(score_txt, (10, 10))
        if player.shield_active:
            shield_txt = font.render("SHIELD ACTIVE", True, (0, 255, 255))
            screen.blit(shield_txt, (10, 40))

    elif state == "MENU":
        screen.fill(BLACK)
        draw_button(screen, "PLAY", 100, 250, 200, 50, (0, 128, 0))
        
    elif state == "GAMEOVER":
        screen.fill((150, 0, 0))
        font = pygame.font.SysFont("Arial", 50)
        go_txt = font.render("GAME OVER", True, WHITE)
        screen.blit(go_txt, (WIDTH//2 - 120, HEIGHT//2 - 50))
        draw_button(screen, "RETRY", 100, 400, 200, 50, BLACK)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
