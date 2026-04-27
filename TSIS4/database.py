import psycopg2

class Database:
    def __init__(self):
        try:
            self.conn = psycopg2.connect(
                dbname="snake_db", 
                user="postgres", 
                password="your_password", 
                host="localhost"
            )
            self.cur = self.conn.cursor()
            self._create_tables()
        except Exception as e:
            print(f"Database error: {e}")
            self.conn = None

    def _create_tables(self):
        if not self.conn: return
        self.cur.execute("""
            CREATE TABLE IF NOT EXISTS players (
                id SERIAL PRIMARY KEY,
                username VARCHAR(50) UNIQUE NOT NULL
            );
            CREATE TABLE IF NOT EXISTS game_sessions (
                id SERIAL PRIMARY KEY,
                player_id INTEGER REFERENCES players(id),
                score INTEGER NOT NULL,
                level_reached INTEGER NOT NULL,
                played_at TIMESTAMP DEFAULT NOW()
            );
        """)
        self.conn.commit()

    def save_game(self, username, score, level):
        if not self.conn: return
        
        self.cur.execute("INSERT INTO players (username) VALUES (%s) ON CONFLICT (username) DO NOTHING", (username,))
        
        
        self.cur.execute("SELECT id FROM players WHERE username = %s", (username,))
        p_id = self.cur.fetchone()[0]
        
        self.cur.execute("INSERT INTO game_sessions (player_id, score, level_reached) VALUES (%s, %s, %s)", 
                         (p_id, score, level))
        self.conn.commit()

    def get_top_10(self):
        if not self.conn: return []
        self.cur.execute("""
            SELECT p.username, s.score, s.level_reached, s.played_at 
            FROM game_sessions s 
            JOIN players p ON s.player_id = p.id 
            ORDER BY s.score DESC 
            LIMIT 10
        """)
        return self.cur.fetchall()

    
    def get_personal_best(self, username):
        if not self.conn: return 0
        self.cur.execute("""
            SELECT MAX(s.score) 
            FROM game_sessions s 
            JOIN players p ON s.player_id = p.id 
            WHERE p.username = %s
        """, (username,))
        result = self.cur.fetchone()[0]
        return result if result else 0

    def close(self):
        if self.conn:
            self.cur.close()
            self.conn.close()
