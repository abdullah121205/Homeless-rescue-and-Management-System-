import os
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash

# Connect to database
def connect_db():
    # Configure globally to return rows as dictionary objects
    conn = psycopg2.connect(
        os.environ["DATABASE_URL"], 
        connection_factory=psycopg2.extras.RealDictConnection
    )
    return conn

# Create tables
def create_tables():
    conn = connect_db()
    cursor = conn.cursor()

    # User table
    # CHANGED: AUTOINCREMENT replaced with SERIAL
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users(
       id SERIAL PRIMARY KEY,
       fullname TEXT NOT NULL,
       username TEXT UNIQUE NOT NULL,
       email TEXT UNIQUE NOT NULL,
       password TEXT NOT NULL
    )
    """)

    # Homeless Person Table
    # CHANGED: AUTOINCREMENT replaced with SERIAL
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS persons(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        alias TEXT,
        age INTEGER,
        gender TEXT,
        rescue_date TEXT,
        location TEXT,
        rescued_by TEXT,
        status TEXT,
        physical_condition TEXT,
        medical_issues TEXT,
        disability TEXT,
        aadhaar TEXT,
        family_contact TEXT,
        remarks TEXT,
        photo TEXT
    )
    """)
    
    # Staff Table  
    # CHANGED: AUTOINCREMENT replaced with SERIAL
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT,
        phone TEXT,
        email TEXT,
        joining_date TEXT,
        address TEXT
    )
    """)

    conn.commit()
    cursor.close()
    conn.close()


# Insert Person
def insert_person(
    name,
    alias,
    age,
    gender,
    rescue_date,
    location,
    rescued_by,
    status,
    physical_condition,
    medical_issues,
    disability,
    aadhaar,
    family_contact,
    remarks,
    photo
):
    conn = connect_db()
    cursor = conn.cursor()

    # CHANGED: SQLite "?" placeholders changed to PostgreSQL "%s" placeholders
    cursor.execute("""
    INSERT INTO persons(
        name,
        alias,
        age,
        gender,
        rescue_date,
        location,
        rescued_by,
        status,
        physical_condition,
        medical_issues,
        disability,
        aadhaar,
        family_contact,
        remarks,
        photo
    )
    VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """, (
        name,
        alias,
        age,
        gender,
        rescue_date,
        location,
        rescued_by,
        status,
        physical_condition,
        medical_issues,
        disability,
        aadhaar,
        family_contact,
        remarks,
        photo
    ))

    conn.commit()
    cursor.close()
    conn.close()


# Get One Person
def get_person(id):
    conn = connect_db()
    cursor = conn.cursor()

    # CHANGED: "?" to "%s"
    cursor.execute("""
    SELECT * FROM persons
    WHERE id=%s
    """, (id,))

    person = cursor.fetchone()

    cursor.close()
    conn.close()

    return person
    

# View Persons
def get_all_persons():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM persons")
    data = cursor.fetchall()

    cursor.close()
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

    cursor.close()
    conn.close()

    return persons
    

# Total Persons
def get_total_persons():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM persons")

    # RealDictConnection returns row dictionaries; unpack to get the raw aggregate value
    total = list(cursor.fetchone().values())[0]
    cursor.close()
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

    total = list(cursor.fetchone().values())[0]

    cursor.close()
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

    total = list(cursor.fetchone().values())[0]

    cursor.close()
    conn.close()

    return total


def get_total_volunteers():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM staff")

    total = list(cursor.fetchone().values())[0] 

    cursor.close()
    conn.close()

    return total
     

# Update Person
def update_person(
    id,
    name,
    alias,
    age,
    gender,
    rescue_date,
    location,
    rescued_by,
    status,
    physical_condition,
    medical_issues,
    disability,
    aadhaar,
    family_contact,
    remarks,
    photo
):
    conn = connect_db()
    cursor = conn.cursor()

    # CHANGED: "?" to "%s"
    cursor.execute("""
    UPDATE persons
    SET
        name=%s,
        alias=%s,
        age=%s,
        gender=%s,
        rescue_date=%s,
        location=%s,
        rescued_by=%s,
        status=%s,
        physical_condition=%s,
        medical_issues=%s,
        disability=%s,
        aadhaar=%s,
        family_contact=%s,
        remarks=%s,
        photo=%s
    WHERE id=%s
    """, (
        name,
        alias,
        age,
        gender,
        rescue_date,
        location,
        rescued_by,
        status,
        physical_condition,
        medical_issues,
        disability,
        aadhaar,
        family_contact,
        remarks,
        photo,
        id
    ))
    conn.commit()
    cursor.close()
    conn.close()


# Delete Person
def delete_person(id):
    conn = connect_db()
    cursor = conn.cursor()

    # CHANGED: "?" to "%s"
    cursor.execute("DELETE FROM persons WHERE id=%s", (id,))

    conn.commit()
    cursor.close()
    conn.close()


# Search Person
def search_person(keyword):
    conn = connect_db()
    cursor = conn.cursor()

    # CHANGED: "?" to "%s"
    cursor.execute("""
    SELECT * FROM persons
    WHERE name LIKE %s
       OR location LIKE %s
    """, ('%' + keyword + '%',
          '%' + keyword + '%'))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


def filter_by_status(status):
    conn = connect_db()
    cursor = conn.cursor()

    # CHANGED: "?" to "%s"
    cursor.execute("""
    SELECT * FROM persons
    WHERE status = %s
    """, (status,))

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    return data


# Register User
def insert_user(fullname, username, email, password):
    conn = connect_db()
    cursor = conn.cursor()

    hashed_password = generate_password_hash(password)

    # CHANGED: "?" to "%s"
    cursor.execute("""
    INSERT INTO users(fullname, username, email, password)
    VALUES (%s, %s, %s, %s)
    """, (fullname, username, email, hashed_password))

    conn.commit()
    cursor.close()
    conn.close()


# Login User
def login_user(username, password):
    conn = connect_db()
    cursor = conn.cursor()

    # CHANGED: "?" to "%s"
    cursor.execute("""
    SELECT * FROM users
    WHERE username=%s
    """, (username,))

    user = cursor.fetchone()

    cursor.close()
    conn.close()

    if user and check_password_hash(user["password"], password):
        return user

    return None


# Insert Staff
def insert_staff(name, role, phone, email, joining_date, address):
    conn = connect_db()
    cursor = conn.cursor()

    # CHANGED: "?" to "%s"
    cursor.execute("""
    INSERT INTO staff(
        name,
        role,
        phone,
        email,
        joining_date,
        address
    )
    VALUES(%s, %s, %s, %s, %s, %s)
    """, (
        name,
        role,
        phone,
        email,
        joining_date,
        address
    ))

    conn.commit()
    cursor.close()
    conn.close()


# View All Staff
def get_all_staff():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM staff")
    data = cursor.fetchall()

    cursor.close()
    conn.close()
    return data


# Get Single Staff
def get_staff(id):
    conn = connect_db()
    cursor = conn.cursor()

    # CHANGED: "?" to "%s"
    cursor.execute("""
    SELECT * FROM staff
    WHERE id=%s
    """, (id,))

    staff = cursor.fetchone()

    cursor.close()
    conn.close()
    return staff


# Update Staff
def update_staff(
    id,
    name,
    role,
    phone,
    email,
    joining_date,
    address
):
    conn = connect_db()
    cursor = conn.cursor()

    # CHANGED: "?" to "%s"
    cursor.execute("""
    UPDATE staff
    SET
        name=%s,
        role=%s,
        phone=%s,
        email=%s,
        joining_date=%s,
        address=%s
    WHERE id=%s
    """, (
        name,
        role,
        phone,
        email,
        joining_date,
        address,
        id
    ))

    conn.commit()
    cursor.close()
    conn.close()


# Delete Staff
def delete_staff(id):
    conn = connect_db()
    cursor = conn.cursor()

    # CHANGED: "?" to "%s"
    cursor.execute("""
    DELETE FROM staff
    WHERE id=%s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()


# Total Staff Count
def get_total_staff():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM staff")
    total = list(cursor.fetchone().values())[0]

    cursor.close()
    conn.close()
    return total


# Active Staff Count
def get_active_staff():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM staff")
    total = list(cursor.fetchone().values())[0]

    cursor.close()
    conn.close()
    return total


# Total Roles
def get_total_roles():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COUNT(DISTINCT role)
    FROM staff
    """)
    total = list(cursor.fetchone().values())[0]

    cursor.close()
    conn.close()
    return total


# ---------------- VOLUNTEER ACCOUNTS ----------------

def get_all_volunteers():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, fullname, username, email
        FROM users
        ORDER BY id
    """)
    volunteers = cursor.fetchall()

    cursor.close()
    conn.close()
    return volunteers


def delete_volunteer(id):
    conn = connect_db()
    cursor = conn.cursor()

    # CHANGED: "?" to "%s"
    cursor.execute("""
        DELETE FROM users
        WHERE id=%s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()


if __name__ == "__main__":
    create_tables()
    print("Database created successfully.")
