import sqlite3
import hashlib
from datetime import datetime

# Veritabanı bağlantısı
conn = sqlite3.connect("gunluk.db", check_same_thread=False)
c = conn.cursor()

# Tablolar
c.execute("""
CREATE TABLE IF NOT EXISTS users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT UNIQUE,
    password_hash TEXT
)
""")

c.execute("""
CREATE TABLE IF NOT EXISTS entries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER,
    title TEXT,
    content TEXT,
    mood TEXT,
    created_at TEXT
)
""")

conn.commit()


def hash_password(password: str) -> str:
    return hashlib.sha256(password.encode()).hexdigest()


def register_user(username: str, password: str) -> bool:
    try:
        c.execute(
            "INSERT INTO users (username, password_hash) VALUES (?, ?)",
            (username, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError:
        return False


def login_user(username: str, password: str):
    c.execute(
        "SELECT * FROM users WHERE username=? AND password_hash=?",
        (username, hash_password(password))
    )
    return c.fetchone()


def add_entry(user_id: int, title: str, content: str, mood: str):
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M")
    c.execute(
        "INSERT INTO entries (user_id, title, content, mood, created_at) VALUES (?, ?, ?, ?, ?)",
        (user_id, title, content, mood, created_at)
    )
    conn.commit()


def get_entries(user_id: int):
    c.execute(
        "SELECT * FROM entries WHERE user_id=? ORDER BY id DESC",
        (user_id,)
    )
    return c.fetchall()


def delete_entry(entry_id: int):
    c.execute("DELETE FROM entries WHERE id=?", (entry_id,))
    conn.commit()


def update_entry(entry_id: int, title: str, content: str, mood: str):
    c.execute(
        "UPDATE entries SET title=?, content=?, mood=? WHERE id=?",
        (title, content, mood, entry_id)
    )
    conn.commit()
