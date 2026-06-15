import sqlite3

DB_PATH = "data/pets.db"

# ---------------- CONNECT ----------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


# ---------------- CREATE TABLE ----------------
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            breed TEXT,
            weight REAL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- INSERT PET ----------------
def add_pet(name, age, breed, weight):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pets (name, age, breed, weight)
        VALUES (?, ?, ?, ?)
    """, (name, age, breed, weight))

    conn.commit()
    conn.close()


# ---------------- GET ALL PETS ----------------
def get_pets():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pets")
    rows = cursor.fetchall()

    conn.close()
=======
import sqlite3

DB_PATH = "data/pets.db"

# ---------------- CONNECT ----------------
def get_connection():
    conn = sqlite3.connect(DB_PATH)
    return conn


# ---------------- CREATE TABLE ----------------
def create_table():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            breed TEXT,
            weight REAL
        )
    """)

    conn.commit()
    conn.close()


# ---------------- INSERT PET ----------------
def add_pet(name, age, breed, weight):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        INSERT INTO pets (name, age, breed, weight)
        VALUES (?, ?, ?, ?)
    """, (name, age, breed, weight))

    conn.commit()
    conn.close()


# ---------------- GET ALL PETS ----------------
def get_pets():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM pets")
    rows = cursor.fetchall()

    conn.close()
    return rows
