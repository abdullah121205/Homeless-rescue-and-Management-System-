import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

# Connect to database
def connect_db():
    conn = sqlite3.connect("database.db")
    conn.row_factory = sqlite3.Row
    return conn


# Create tables
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # User  table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
       id INTEGER PRIMARY KEY AUTOINCREMENT,
       fullname TEXT NOT NULL,
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
    status TEXT,
    photo TEXT
    )
    """)

    conn.commit()
    conn.close()


# Insert Person
def insert_person(name, age, gender, location, status, photo):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO persons(name, age, gender, location, status, photo)
    VALUES (?, ?, ?, ?, ?, ?)
    """, (name, age, gender, location, status, photo))

    conn.commit()
    conn.close()


# Get One Person
def get_person(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM persons
    WHERE id=?
    """, (id,))

    person = cursor.fetchone()

    conn.close()

    return person
    

# View Persons
def get_all_persons():
    conn = connect_db()
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM persons")
    data = cursor.fetchall()

    conn.close()
    return data

# Recent Persons
def get_recent_persons():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT *
        FROM persons
        ORDER BY id DESC
        LIMIT 5
    """)

    persons = cursor.fetchall()

    conn.close()

    return persons
    
# Total Persons
def get_total_persons():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM persons")

    total = cursor.fetchone()[0]

    conn.close()

    return total


# Total Pending Cases
def get_pending_cases():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM persons
        WHERE status != 'Reunited'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total


# Total Rescued Persons
def get_rescued_count():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT COUNT(*)
        FROM persons
        WHERE status='Rescued'
    """)

    total = cursor.fetchone()[0]

    conn.close()

    return total
    
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

# Register User
def insert_user(fullname, username, email, password):
    conn = connect_db()
    cursor = conn.cursor()

    hashed_password = generate_password_hash(password)

    cursor.execute("""
    INSERT INTO users(fullname, username, email, password)
    VALUES (?, ?, ?, ?)
    """, (fullname, username, email, hashed_password))

    conn.commit()
    conn.close()


# Login User
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM users
    WHERE username=?
    """, (username,))

    user = cursor.fetchone()

    conn.close()

    if user and check_password_hash(user["password"], password):
        return user

    return None

if __name__ == "__main__":
    create_tables()
    print("Database created successfully.")
