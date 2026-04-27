
state = "MENU" 

while True:
    if state == "MENU":
        state = show_main_menu() # Функция из ui.py возвращает выбранное действие
    elif state == "GAME":
        results = start_game_loop() # Сама игра
        state = "GAMEOVER"
    elif state == "SETTINGS":
        state = show_settings()
