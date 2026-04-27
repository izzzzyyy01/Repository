import pygame
import datetime
from constants import *
from tools import flood_fill, draw_text

pygame.init()
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
canvas = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
canvas.fill(WHITE)

current_size = 5
current_color = BLACK
drawing = False
last_pos = None

# Для текста
text_active = False
text_content = ""
text_pos = (0, 0)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Смена размера кисти (1, 2, 3)
        if event.type == pygame.KEYDOWN:
            if event.key in BRUSH_SIZES:
                current_size = BRUSH_SIZES[event.key]
            
            # Сохранение Ctrl+S
            if event.key == pygame.K_s and (pygame.key.get_mods() & pygame.KMOD_CTRL):
                name = f"../saves/paint_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
                pygame.image.save(canvas, name)
                print("Saved!")

            # Обработка ввода текста
            if text_active:
                if event.key == pygame.K_RETURN:
                    draw_text(canvas, text_content, text_pos, current_color)
                    text_active = False
                    text_content = ""
                elif event.key == pygame.K_ESCAPE:
                    text_active = False
                elif event.key == pygame.K_BACKSPACE:
                    text_content = text_content[:-1]
                else:
                    text_content += event.unicode

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # ЛКМ
                if not text_active:
                    drawing = True
                    last_pos = event.pos
                else:
                    text_pos = event.pos

        if event.type == pygame.MOUSEBUTTONUP:
            drawing = False

        if event.type == pygame.MOUSEMOTION and drawing:
         
            pygame.draw.line(canvas, current_color, last_pos, event.pos, current_size)
            last_pos = event.pos

    screen.blit(canvas, (0, 0))
    if text_active:
        draw_text(screen, text_content + "|", text_pos, current_color)
    
    pygame.display.flip()

pygame.quit()
