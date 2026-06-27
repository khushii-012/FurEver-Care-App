import sqlite3
import os

DB_PATH = "data/pets.db"
os.makedirs("data", exist_ok=True)


def get_connection():
    return sqlite3.connect(DB_PATH)


def create_table():
    conn = get_connection()
    c = conn.cursor()

    c.execute("""
        CREATE TABLE IF NOT EXISTS pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT,
            age INTEGER,
            breed TEXT,
            weight REAL,
            photo BLOB,
            species TEXT DEFAULT 'dog'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS vaccinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_name TEXT,
            vaccine TEXT,
            last_date TEXT,
            next_date TEXT,
            vet_name TEXT
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS missing_pets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            pet_name TEXT,
            species TEXT,
            breed TEXT,
            color TEXT,
            last_seen_location TEXT,
            contact TEXT,
            description TEXT,
            photo BLOB,
            reported_date TEXT,
            status TEXT DEFAULT 'missing'
        )
    """)

    c.execute("""
        CREATE TABLE IF NOT EXISTS rescue_reports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            location TEXT,
            description TEXT,
            severity TEXT,
            lat REAL,
            lon REAL,
            reported_date TEXT,
            status TEXT DEFAULT 'open'
        )
    """)

    conn.commit()
    conn.close()


def add_pet(name, age, breed, weight, photo=None, species='dog'):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO pets (name, age, breed, weight, photo, species) VALUES (?,?,?,?,?,?)",
        (name, age, breed, weight, photo, species)
    )
    conn.commit()
    conn.close()


def get_pets():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM pets")
    rows = c.fetchall()
    conn.close()
    return rows


def delete_pet(pet_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("DELETE FROM pets WHERE id=?", (pet_id,))
    conn.commit()
    conn.close()


def add_vaccination(pet_name, vaccine, last_date, next_date, vet_name):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO vaccinations (pet_name, vaccine, last_date, next_date, vet_name) VALUES (?,?,?,?,?)",
        (pet_name, vaccine, last_date, next_date, vet_name)
    )
    conn.commit()
    conn.close()


def get_vaccinations():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM vaccinations ORDER BY next_date ASC")
    rows = c.fetchall()
    conn.close()
    return rows


def add_missing_pet(pet_name, species, breed, color, last_seen_location, contact, description, photo, reported_date):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        """INSERT INTO missing_pets
           (pet_name, species, breed, color, last_seen_location, contact, description, photo, reported_date)
           VALUES (?,?,?,?,?,?,?,?,?)""",
        (pet_name, species, breed, color, last_seen_location, contact, description, photo, reported_date)
    )
    conn.commit()
    conn.close()


def get_missing_pets():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM missing_pets WHERE status='missing' ORDER BY reported_date DESC")
    rows = c.fetchall()
    conn.close()
    return rows


def mark_pet_found(pet_id):
    conn = get_connection()
    c = conn.cursor()
    c.execute("UPDATE missing_pets SET status='found' WHERE id=?", (pet_id,))
    conn.commit()
    conn.close()


def add_rescue_report(location, description, severity, lat, lon, reported_date):
    conn = get_connection()
    c = conn.cursor()
    c.execute(
        "INSERT INTO rescue_reports (location, description, severity, lat, lon, reported_date) VALUES (?,?,?,?,?,?)",
        (location, description, severity, lat, lon, reported_date)
    )
    conn.commit()
    conn.close()


def get_rescue_reports():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM rescue_reports ORDER BY reported_date DESC LIMIT 10")
    rows = c.fetchall()
    conn.close()
    return rows