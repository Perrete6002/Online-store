import sqlite3 as sql

def createDB():
    conn = sql.connect("users.db")
    conn.commit()
    conn.close()

def createTable():
    conn = sql.connect("users.db")
    cursor = conn.cursor()
    cursor.execute(
        """CREATE TABLE IF NOT EXISTS users (
            username TEXT,
            email TEXT,
            password TEXT
        )"""
    )
    conn.commit()
    conn.close()

def insertRow(username, email, password):
    conn = sql.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, email, password) VALUES (?, ?, ?)", (username, email, password))
    conn.commit()
    conn.close()

def get_user_by_username(username):
    conn = sql.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
    user = cursor.fetchone()
    conn.close()
    print("Retrieved user from database:", user)  # Agregar esta línea para depurar
    return user


def update_user(old_username, new_username, new_email, new_password):
    conn = sql.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET username = ?, email = ?, password = ? WHERE username = ?", (new_username, new_email, new_password, old_username))
    conn.commit()
    conn.close()


def check_table_structure():
    conn = sql.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(users)")
    columns = cursor.fetchall()
    conn.close()
    print(columns)

check_table_structure()
