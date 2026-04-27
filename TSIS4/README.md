# TSIS 4: Advanced Snake Game

Extended version of the classic Snake game with database integration and advanced mechanics.

## Features
- **Database Integration**: Saves scores, levels, and timestamps to PostgreSQL.
- **Leaderboard**: In-game Top 10 high scores display.
- **Poison Food**: Reduces snake length; game over if too short.
- **Power-ups**: Timed speed boosts and shields.
- **Dynamic Obstacles**: Static walls appear starting from Level 3.
- **Persistence**: Game settings (color, grid, sound) are saved in `settings.json`.

## Requirements
- Python 3.x
- Pygame
- psycopg2 (PostgreSQL adapter)

## Setup
1. Create a PostgreSQL database named `snake_db`.
2. Update your credentials in `database.py`.
3. Run the game:
   ```bash
   python main.py
