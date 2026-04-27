import pygame
import json
import datetime
from game_logic import GameLogic
from database import Database


pygame.init()
db = Database()


def load_settings():
    try:
        with open('settings.json', 'r') as f:
            return json.load(f)
    except:
        return {
            "screen_width": 800,
            "screen_height": 600,
            "snake_color": [0, 255, 0],
            "grid": True,
            "sound": True
        }

settings = load_settings()
screen = pygame.display.set_mode((settings['screen_width'], settings['screen_height']))
pygame.display.set_caption("Snake Game: DB Edition")
clock = pygame.time.Clock()
font_main = pygame.font.SysFont("Arial", 32)
font_small = pygame.font.SysFont("Arial", 20)

def draw_text(text, x, y, color=(255, 255, 255), center=False, font=None):
    if font is None: font = font_main
    img = font.render(text, True, color)
    if center:
        rect = img.get_rect(center=(x, y))
        screen.blit(img, rect)
    else:
        screen.blit(img, (x, y))

def main():
    state = "MENU"
    username = ""
    game = None
    personal_best = 0
    running = True

    while running:
        screen.fill((20, 20, 20)) 
        events = pygame.event.get()
        
        for event in events:
            if event.type == pygame.QUIT:
                running = False

    
            if state == "MENU":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN and len(username) > 0:
                        game = GameLogic(settings)
                        personal_best = db.get_personal_best(username)
                        state = "GAME"
                    elif event.key == pygame.K_l: 
                        state = "LEADERBOARD"
                    elif event.key == pygame.K_s:
                        state = "SETTINGS"
                    elif event.key == pygame.K_BACKSPACE:
                        username = username[:-1]
                    else:
                        if len(username) < 15 and event.unicode.isalnum():
                            username += event.unicode

         
            elif state == "GAME":
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP and game.snake.dir != "DOWN":
                        game.snake.dir = "UP"
                    elif event.key == pygame.K_DOWN and game.snake.dir != "UP":
                        game.snake.dir = "DOWN"
                    elif event.key == pygame.K_LEFT and game.snake.dir != "RIGHT":
                        game.snake.dir = "LEFT"
                    elif event.key == pygame.K_RIGHT and game.snake.dir != "LEFT":
                        game.snake.dir = "RIGHT"

           
            elif state in ["LEADERBOARD", "SETTINGS", "GAME_OVER"]:
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_b or event.key == pygame.K_ESCAPE:
                        state = "MENU"

 
        if state == "MENU":
            draw_text("SNAKE DATABASE PRO", 400, 150, (0, 255, 0), center=True)
            draw_text(f"Username: {username}_", 400, 250, center=True)
            draw_text("[ENTER] Play  [L] Leaderboard  [S] Settings", 400, 450, (150, 150, 150), center=True, font=font_small)

        elif state == "GAME":
            game.update()
            
           
            if settings['grid']:
                for x in range(0, settings['screen_width'], 20):
                    pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, settings['screen_height']))
                for y in range(0, settings['screen_height'], 20):
                    pygame.draw.line(screen, (40, 40, 40), (0, y), (settings['screen_width'], y))

      
            for obs in game.obstacles:
                pygame.draw.rect(screen, (120, 120, 120), (obs[0], obs[1], 18, 18))
            
        
            for i, seg in enumerate(game.snake.body):
                color = tuple(settings['snake_color'])
                if i == 0: color = (255, 255, 255) 
                pygame.draw.rect(screen, color, (seg[0], seg[1], 18, 18))

            # Еда
            for f in game.foods:
                pygame.draw.rect(screen, f.color, (f.pos[0], f.pos[1], 18, 18))

          
            draw_text(f"Score: {game.score} | Level: {game.level} | Best: {personal_best}", 10, 10, font=font_small)
            
            if game.game_over:
                db.save_game(username, game.score, game.level)
                state = "GAME_OVER"

        elif state == "GAME_OVER":
            draw_text("GAME OVER", 400, 250, (255, 50, 50), center=True)
            draw_text(f"Final Score: {game.score}", 400, 300, center=True)
            draw_text("Press [B] for Menu", 400, 400, (150, 150, 150), center=True, font=font_small)

        elif state == "LEADERBOARD":
            draw_text("TOP 10 ALL TIME", 400, 80, (255, 215, 0), center=True)
            top_scores = db.get_top_10()
            for i, (name, sc, lvl) in enumerate(top_scores):
                draw_text(f"{i+1}. {name}: {sc} (Lvl {lvl})", 250, 150 + i*35, font=font_small)
            draw_text("Press [B] to Back", 400, 550, center=True, font=font_small)

        elif state == "SETTINGS":
            draw_text("SETTINGS", 400, 100, center=True)
            grid_status = "ON" if settings['grid'] else "OFF"
            draw_text(f"Press [G] to toggle Grid: {grid_status}", 400, 250, center=True, font=font_small)
            
            
            keys = pygame.key.get_pressed()
            if keys[pygame.K_g]: 
                settings['grid'] = not settings['grid']
                pygame.time.delay(150) 
            
            draw_text("Press [B] to Save & Back", 400, 450, (0, 255, 0), center=True, font=font_small)
            with open('settings.json', 'w') as f:
                json.dump(settings, f)

        pygame.display.flip()
        
        speed = 10 + (game.level * 2 if game else 0)
        clock.tick(speed)

    db.close()
    pygame.quit()

if __name__ == "__main__":
    main()
