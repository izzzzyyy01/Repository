import pygame

def flood_fill(surface, x, y, new_color):
    target_color = surface.get_at((x, y))
    if target_color == new_color:
        return
    
    stack = [(x, y)]
    while stack:
        cx, cy = stack.pop()
        if surface.get_at((cx, cy)) == target_color:
            surface.set_at((cx, cy), new_color)
            if cx + 1 < surface.get_width(): stack.append((cx + 1, cy))
            if cx - 1 >= 0: stack.append((cx - 1, cy))
            if cy + 1 < surface.get_height(): stack.append((cx, cy + 1))
            if cy - 1 >= 0: stack.append((cx, cy - 1))


def draw_text(surface, text, pos, color, font_size=30):
    font = pygame.font.SysFont("Arial", font_size)
    text_surf = font.render(text, True, color)
    surface.blit(text_surf, pos)
