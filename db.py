import sqlite3
import json

DB_FILE = "ludo_game.db"

def get_connection():
  
    conn = sqlite3.connect(DB_FILE)
    return conn

def init_db():
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE,
            state TEXT
        )
    """)
    conn.commit()
    conn.close()

def save_game(name, game_state):
    
    conn = get_connection()
    c = conn.cursor()
    state_json = json.dumps(game_state)
    c.execute("INSERT OR REPLACE INTO games (name, state) VALUES (?, ?)", (name, state_json))
    conn.commit()
    conn.close()

def load_game(name):
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT state FROM games WHERE name=?", (name,))
    row = c.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    return None

def list_games():
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT name FROM games")
    rows = c.fetchall()
    conn.close()
    return [r[0] for r in rows]

def delete_game(name):
    
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM games WHERE name=?", (name,))
    conn.commit()
    conn.close()
