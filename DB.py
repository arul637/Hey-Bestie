import sqlite3

DB_NAME = "users.db"

# Initialize database and table (if not exists)
def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT NOT NULL,
            email TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            gender TEXT,
            mobile TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Register a new user
def register_user(username, email, password, gender, mobile):
    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO users (username, email, password, gender, mobile)
            VALUES (?, ?, ?, ?, ?)
        ''', (username, email, password, gender, mobile))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        # Email already exists
        return False

# Validate login credentials
def validate_login(email, password):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE email = ? AND password = ?', (email, password))
    user = cursor.fetchone()
    conn.close()
    return user  