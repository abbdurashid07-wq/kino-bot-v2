import sqlite3

db = sqlite3.connect("kino.db", check_same_thread=False)
cursor = db.cursor()

# Kinolar jadvali
cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    code TEXT PRIMARY KEY,
    file_id TEXT
)
""")

# Foydalanuvchilar jadvali
cursor.execute("""
CREATE TABLE IF NOT EXISTS users (
    user_id INTEGER PRIMARY KEY
)
""")

db.commit()


# Kino qo'shish
def add_movie(code, file_id):
    cursor.execute(
        "INSERT OR REPLACE INTO movies (code, file_id) VALUES (?, ?)",
        (code, file_id)
    )
    db.commit()


# Kino olish
def get_movie(code):
    cursor.execute(
        "SELECT file_id FROM movies WHERE code = ?",
        (code,)
    )

    result = cursor.fetchone()

    if result:
        return result[0]

    return None


# Foydalanuvchi qo'shish
def add_user(user_id):
    cursor.execute(
        "INSERT OR IGNORE INTO users (user_id) VALUES (?)",
        (user_id,)
    )
    db.commit()


# Barcha foydalanuvchilar
def get_users():
    cursor.execute("SELECT user_id FROM users")
    return [row[0] for row in cursor.fetchall()]


# Foydalanuvchilar soni
def user_count():
    cursor.execute("SELECT COUNT(*) FROM users")
    return cursor.fetchone()[0]


# Kino o'chirish
def delete_movie(code):
    cursor.execute(
        "DELETE FROM movies WHERE code = ?",
        (code,)
    )
    db.commit()
