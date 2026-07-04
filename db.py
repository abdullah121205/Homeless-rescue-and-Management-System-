import sqlite3

# Connect to database
def connect_db():
    conn = sqlite3.connect("database.db")
    return conn


# Create tables
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # User Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        password TEXT NOT NULL
    )
    """)

    # Homeless Person Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS persons(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        location TEXT,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()


# Insert Person
def insert_person(name, age, gender, location, status):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO persons(name, age, gender, location,status)
    VALUES (?, ?, ?, ?)
    """, (name, age, gender, location,status))

    conn.commit()
    conn.close()


# View Persons
def get_all_persons():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM persons")
    data = cursor.fetchall()

    conn.close()
    return data


# Update Person
def update_person(id, name, age, gender, location,status):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE persons
    SET name=?, age=?, gender=?, location=?, status=?
    WHERE id=?
    """, (name, age, gender, location, status, id))

    conn.commit()
    conn.close()


# Delete Person
def delete_person(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM persons WHERE id=?", (id,))

    conn.commit()
    conn.close()


# Search Person
def search_person(keyword):

    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM persons
    WHERE name LIKE ?
       OR location LIKE ?
    """, ('%' + keyword + '%',
          '%' + keyword + '%'))

    data = cursor.fetchall()

    conn.close()

    return data

def filter_by_status(status):

    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM persons
    WHERE status = ?
    """, (status,))

    data = cursor.fetchall()

    conn.close()

    return data

if __name__ == "__main__":
    create_tables()
    print("Database created successfully.")
