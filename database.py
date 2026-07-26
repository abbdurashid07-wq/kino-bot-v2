import sqlite3

db = sqlite3.connect("kino.db", check_same_thread=False)
cursor = db.cursor()

# Kinolar jadvali
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    code TEXT PRIMARY KEY,
    file_id TEXT NOT NULL
)
""")

# Foydalanuvchilar jadvali
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")

db.commit()


# =======================
# KINOLAR
# =======================

def add_movie(code, file_id):
    cursor.execute(
        "INSERT OR REPLACE INTO movies (code, file_id) VALUES (?, ?)",
        (code, file_id)
    )
    db.commit()


def get_movie(code):
    cursor.execute(
        "SELECT file_id FROM movies WHERE code = ?",
        (code,)
    )
    result = cursor.fetchone()
    return result[0] if result else None


def delete_movie(code):
    cursor.execute(
        "DELETE FROM movies WHERE code = ?",
        (code,)
    )
    db.commit()


# =======================
# FOYDALANUVCHILAR
# =======================

def add_user(user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,)
    )
    db.commit()


def get_users():
    cursor.execute("SELECT user_id FROM users")
    return [row[0] for row in cursor.fetchall()]


def user_count():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]
