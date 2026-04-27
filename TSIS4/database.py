import psycopg2

class Database:
    def __init__(self):
       
        self.conn = psycopg2.connect(
            dbname="snake_db",
            user="postgres",
            password="your_password",
            host="localhost",
            port="5432"
        )
        self.cur = self.conn.cursor()
        self._create_tables()

    def _create_tables(self):
        """Создает таблицы, если они еще не существуют"""
        commands = (
            """
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            )
            """,
            """
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            )
            """
        )
        for command in commands:
            self.cur.execute(command)
        self.conn.commit()

    def get_user_best(self, username):
        """Возвращает лучший счет игрока"""
        query = """
            SELECT MAX(score) FROM game_sessions s
            JOIN players p ON s.player_id = p.id
            WHERE p.username = %s
        """
        self.cur.execute(query, (username,))
        result = self.cur.fetchone()
        return result[0] if result[0] is not None else 0

    def save_game(self, username, score, level):
        """Сохраняет результат игры"""
       
        self.cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
        self.cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        player_id = self.cur.fetchone()[0]
        
   
        self.cur.execute(
            "INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)",
            (player_id, score, level)
        )
        self.conn.commit()

    def get_top_10(self):
        """Для экрана Leaderboard"""
        query = """
            SELECT p.username, s.score, s.level_reached, s.played_at 
            FROM game_sessions s 
            JOIN players p ON s.player_id = p.id 
            ORDER BY s.score DESC LIMIT 10
        """
        self.cur.execute(query)
        return self.cur.fetchall()
