import sqlite3

db = sqlite3.connect("kino.db", check_same_thread=False)
cursor = db.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS movies (
    code TEXT PRIMARY KEY,
    file_id TEXT
)
""")

db.commit()


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

    if result:
        return result[0]

    return None
