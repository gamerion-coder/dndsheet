import sqlite3
from flask import g # Import g to use with get_db

DATABASE = '/home/gamerion_agent/.openclaw/shared-workspace/dndsheet/data/dndsheet.db'

def init_db(app):
    with app.app_context():
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS characters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                race TEXT,
                class TEXT,
                level INTEGER,
                strength INTEGER,
                dexterity INTEGER,
                constitution INTEGER,
                intelligence INTEGER,
                wisdom INTEGER,
                charisma INTEGER,
                hp INTEGER,
                ac INTEGER,
                inventory TEXT
            )
        ''')
        conn.commit()

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # This makes rows behave like dictionaries
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()
