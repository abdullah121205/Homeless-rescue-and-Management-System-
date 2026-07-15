import os
import psycopg2
import psycopg2.extras
from werkzeug.security import generate_password_hash, check_password_hash

# Connect to database
def connect_db():
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
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS persons(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        alias TEXT,
        age INTEGER,
        gender TEXT,
        rescue_date TEXT,
        location TEXT,
        rescued_by "SABARMATI NGO RESCUE TEAM",
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
    
    # Staff 
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS staff(
        id SERIAL PRIMARY KEY,
        name TEXT NOT NULL,
        role TEXT,
        phone TEXT,
        email TEXT,
        joining_date DATE,
        address TEXT
    )
    """)

    # Donation Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS donations(
         id SERIAL PRIMARY KEY,
         donor_name TEXT NOT NULL,
         donation_type TEXT NOT NULL,
         amount DECIMAL(10,2) NOT NULL,
         donated_on DATE NOT NULL,
         remarks TEXT
    )
    """)

    # Expense Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS expenses(
        id SERIAL PRIMARY KEY,
        purpose TEXT NOT NULL,
        amount DECIMAL(10,2) NOT NULL,
        spent_on DATE NOT NULL,
        paid_to TEXT NOT NULL,
        remarks TEXT
    )
    """)
    
    # Projects Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS projects(
        id SERIAL PRIMARY KEY,
        project_name TEXT NOT NULL,
        description TEXT,
        start_date TEXT,
        end_date TEXT,
        location TEXT,
        budget INTEGER,
        status TEXT
    )
    """)
    
    # Beneficiaries Table
    # FIXED: Moved inside the open database connection window
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS beneficiaries(
        id SERIAL PRIMARY KEY,
        beneficiary_name TEXT NOT NULL,
        age INTEGER,
        gender TEXT,
        phone TEXT,
        address TEXT,
        project_name TEXT,
        support_type TEXT,
        registration_date TEXT
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
    cursor.execute("SELECT COUNT(*) AS total FROM users")
    result = cursor.fetchone()
    cursor.close()
    conn.close()
    return result["total"]
     
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
    cursor.execute("DELETE FROM persons WHERE id=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()

# Search Person
def search_person(keyword):
    conn = connect_db()
    cursor = conn.cursor()
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

def insert_project(
    project_name,
    description,
    start_date,
    end_date,
    location,
    budget,
    status
):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO projects(
        project_name,
        description,
        start_date,
        end_date,
        location,
        budget,
        status
    )
    VALUES(%s,%s,%s,%s,%s,%s,%s)
    """,(
        project_name,
        description,
        start_date,
        end_date,
        location,
        budget,
        status
    ))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_projects():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT *
    FROM projects
    ORDER BY id DESC
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_project(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT *
    FROM projects
    WHERE id=%s
    """,(id,))
    project = cursor.fetchone()
    cursor.close()
    conn.close()
    return project

def update_project(
    id,
    project_name,
    description,
    start_date,
    end_date,
    location,
    budget,
    status
):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE projects
    SET
        project_name=%s,
        description=%s,
        start_date=%s,
        end_date=%s,
        location=%s,
        budget=%s,
        status=%s
    WHERE id=%s
    """,(
        project_name,
        description,
        start_date,
        end_date,
        location,
        budget,
        status,
        id
    ))
    conn.commit()
    cursor.close()
    conn.close()

def delete_project(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM projects
    WHERE id=%s
    """,(id,))
    conn.commit()
    cursor.close()
    conn.close()

# FIXED: Standardized case structure across searches (using ILIKE/LIKE dynamically context-depending)
def search_project(keyword):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT *
    FROM projects
    WHERE project_name ILIKE %s
       OR location ILIKE %s
    """,(
        "%" + keyword + "%",
        "%" + keyword + "%"
    ))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_total_projects():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(*)
    FROM projects
    """)
    total = list(cursor.fetchone().values())[0]
    cursor.close()
    conn.close()
    return total

def get_active_projects():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(*)
    FROM projects
    WHERE status='Active'
    """)
    total = list(cursor.fetchone().values())[0]
    cursor.close()
    conn.close()
    return total

def get_completed_projects():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(*)
    FROM projects
    WHERE status='Completed'
    """)
    total = list(cursor.fetchone().values())[0]
    cursor.close()
    conn.close()
    return total

def insert_beneficiary(
    beneficiary_name,
    age,
    gender,
    phone,
    address,
    project_name,
    support_type,
    registration_date
):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO beneficiaries(
        beneficiary_name,
        age,
        gender,
        phone,
        address,
        project_name,
        support_type,
        registration_date
    )
    VALUES(%s,%s,%s,%s,%s,%s,%s,%s)
    """,(
        beneficiary_name,
        age,
        gender,
        phone,
        address,
        project_name,
        support_type,
        registration_date
    ))
    conn.commit()
    cursor.close()
    conn.close()

def get_all_beneficiaries():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT *
    FROM beneficiaries
    ORDER BY id DESC
    """)
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data
    
# FIXED: Fixed the structural block and adjusted indentation level
def get_beneficiary(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT *
    FROM beneficiaries
    WHERE id=%s
    """,(id,))
    beneficiary = cursor.fetchone()
    cursor.close()
    conn.close()
    return beneficiary

def update_beneficiary(
    id,
    beneficiary_name,
    age,
    gender,
    phone,
    address,
    project_name,
    support_type,
    registration_date
):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE beneficiaries
    SET
        beneficiary_name=%s,
        age=%s,
        gender=%s,
        phone=%s,
        address=%s,
        project_name=%s,
        support_type=%s,
        registration_date=%s
    WHERE id=%s
    """,(
        beneficiary_name,
        age,
        gender,
        phone,
        address,
        project_name,
        support_type,
        registration_date,
        id
    ))
    conn.commit()
    cursor.close()
    conn.close()

def delete_beneficiary(id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    DELETE FROM beneficiaries
    WHERE id=%s
    """,(id,))
    conn.commit()
    cursor.close()
    conn.close()

def search_beneficiary(keyword):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT *
    FROM beneficiaries
    WHERE beneficiary_name ILIKE %s
       OR project_name ILIKE %s
    """,(
        "%" + keyword + "%",
        "%" + keyword + "%"
    ))
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return data

def get_total_beneficiaries():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("""
    SELECT COUNT(*)
    FROM beneficiaries
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
    cursor.execute("""
        DELETE FROM users
        WHERE id=%s
    """, (id,))
    conn.commit()
    cursor.close()
    conn.close()

# ---------------- FINANCE MODULE ----------------

# Insert Donation

def insert_donation(
     donor_name,
     donation_type,
     amount,
     donated_on,
     remarks
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO donations(
        donor_name,
        donation_type,
        amount,
        donated_on,
        remarks
    )
    VALUES(%s, %s, %s, %s, %s)
    """, (
        donor_name,
        donation_type,
        amount,
        donated_on,
        remarks
    ))

    conn.commit()
    cursor.close()
    conn.close()


 #  all donation

def get_all_donations():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT * FROM donations
    ORDER BY donated_on DESC
    """)

    donations = cursor.fetchall()

    cursor.close()
    conn.close()

    return donations

# Get One Donation

def get_donation(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM donations
    WHERE id=%s
    """, (id,))

    donation = cursor.fetchone()

    cursor.close()
    conn.close()

    return donation

# Update Donation

def update_donation(
    id,
    donor_name,
    donation_type,
    amount,
    donated_on,
    remarks
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE donations
    SET
        donor_name=%s,
        donation_type=%s,
        amount=%s,
        donated_on=%s,
        remarks=%s
    WHERE id=%s
    """, (
        donor_name,
        donation_type,
        amount,
        donated_on,
        remarks,
        id
    ))

    conn.commit()
    cursor.close()
    conn.close()

# delete donation

def delete_donation(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM donations
    WHERE id=%s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()


    # total donation
def get_total_donations():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COALESCE(SUM(amount), 0) AS total
    FROM donations
    """)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result["total"] 

# insert expense

def insert_expense(
    purpose,
    amount,
    spent_on,
    paid_to,
    remarks
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO expenses(
        purpose,
        amount,
        spent_on,
        paid_to,
        remarks
    )
    VALUES(%s, %s, %s, %s, %s)
    """, (
        purpose,
        amount,
        spent_on,
        paid_to,
        remarks
    ))

    conn.commit()
    cursor.close()
    conn.close()

# all expense

def get_all_expenses():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM expenses
    ORDER BY spent_on DESC
    """)

    expenses = cursor.fetchall()

    cursor.close()
    conn.close()

    return expenses 

# Get One Expense

def get_expense(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM expenses
    WHERE id=%s
    """, (id,))

    expense = cursor.fetchone()

    cursor.close()
    conn.close()

    return expense

# Update Expense

def update_expense(
    id,
    purpose,
    amount,
    spent_on,
    paid_to,
    remarks
):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    UPDATE expenses
    SET
        purpose=%s,
        amount=%s,
        spent_on=%s,
        paid_to=%s,
        remarks=%s
    WHERE id=%s
    """, (
        purpose,
        amount,
        spent_on,
        paid_to,
        remarks,
        id
    ))

    conn.commit()
    cursor.close()
    conn.close()

# delete expense

def delete_expense(id):
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    DELETE FROM expenses
    WHERE id=%s
    """, (id,))

    conn.commit()
    cursor.close()
    conn.close()

    # total expense

def get_total_expenses():
    conn = connect_db()
    cursor = conn.cursor()

    cursor.execute("""
    SELECT COALESCE(SUM(amount), 0) AS total
    FROM expenses
    """)

    result = cursor.fetchone()

    cursor.close()
    conn.close()

    return result["total"]  


# Available Balance

def get_available_balance():

    total_donations = get_total_donations()
    total_expenses = get_total_expenses()

    balance = total_donations - total_expenses

    return balance
 
if __name__ == "__main__":
    create_tables()
    print("Database created successfully.")
