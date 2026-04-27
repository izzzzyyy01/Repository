import datetime

def save_canvas(surface):
    # Генерируем имя: paint_20240427_1530.png
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"../saves/paint_{timestamp}.png"
    pygame.image.save(surface, filename)
    print(f"Saved as {filename}")
