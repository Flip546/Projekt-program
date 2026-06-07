
import sqlite3
from flask import g

DATABASE = "movies.db"
SCHEMA_SQL = """
CREATE TABLE IF NOT EXISTS movies(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    title TEXT NOT NULL,
    year TEXT,
    plot TEXT,
    poster_url TEXT,
    watched INTEGER NOT NULL DEFAULT 0 CHECK (watched IN (0, 1)),
    created_at TEXT NOT NULL DEFAULT (datetime('now'))
);
"""

def get_db():
    if "db" not in g:
        conn = sqlite3.connect(DATABASE)
        conn.row_factory = sqlite3.Row
        g.db = conn
    return g.db

def close_db_init(app):
    @app.teardown_appcontext
    def close_db(exception):
        db = g.pop("db", None)
        if db is not None:
            db.close()

def init_db():
    db = get_db()
    db.executescript(SCHEMA_SQL)
    db.commit()

def init_db_command_init(app):
    @app.cli.command("init-db")
    def init_db_command():
        init_db()
        print("✔ Baza filmów zainicjowana!")