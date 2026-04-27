import pygame

def flood_fill(surface, x, y, fill_color):
    target_color = surface.get_at((x, y))
    if target_color == fill_color:
        return
    
    pixels_to_fill = [(x, y)]
    while pixels_to_fill:
        cx, cy = pixels_to_fill.pop()
        if surface.get_at((cx, cy)) == target_color:
            surface.set_at((cx, cy), fill_color)
            # Проверяем соседей (вправо, влево, вверх, вниз)
            if cx + 1 < surface.get_width(): pixels_to_fill.append((cx + 1, cy))
            if cx - 1 >= 0: pixels_to_fill.append((cx - 1, cy))
            if cy + 1 < surface.get_height(): pixels_to_fill.append((cx, cy + 1))
            if cy - 1 >= 0: pixels_to_fill.append((cx, cy - 1))
