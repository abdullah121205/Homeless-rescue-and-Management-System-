import os
import psycopg2
from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
from db import (
    insert_user,
    login_user,
    insert_person,
    get_all_persons,
    get_person,
    update_person,
    search_person,
    filter_by_status,
    delete_person,
    get_total_persons,
    get_pending_cases,
    get_rescued_count,
    get_recent_persons,
    get_total_volunteers,
    get_all_volunteers,
    delete_volunteer,
    insert_staff,
    get_all_staff,
    get_staff,
    update_staff,
    delete_staff,
    get_total_staff,
    get_active_staff,
    get_total_roles
)

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ngo_secret_key")

from db import create_tables

# Initialize tables in the PostgreSQL database if they don't exist yet
create_tables()

# ---------------- LOGIN ----------------

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user = login_user(username, password)

        if user:
            session['user'] = username
            return redirect(url_for('dashboard'))

        return render_template(
            'login.html',
            error="Invalid Username or Password"
        )

    return render_template('login.html')


# ---------------- REGISTER ----------------

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        fullname = request.form['fullname']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        try:
            insert_user(fullname, username, email, password)
            return redirect(url_for('login'))

        except psycopg2.errors.UniqueViolation:
            return render_template(
                'register.html',
                error="Username or Email already exists."
            )

        except Exception as e:
            return render_template(
                'register.html',
                error=str(e)
            )

    return render_template('register.html')


# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():
    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template(
        'dashboard.html',
        total_persons=get_total_persons(),
        rescued=get_rescued_count(),
        pending=get_pending_cases(),
        recent_persons=get_recent_persons(),
        volunteers=get_total_volunteers()
    )
# ---------------- STAFF ----------------


@app.route('/staff')
def staff():

    if 'user' not in session:
        return redirect(url_for('login'))

    staffs = get_all_staff()

    return render_template(
        'staff.html',
        staffs=staffs,
        total_staff=get_total_staff(),
        active_staff=get_active_staff(),
        total_roles=get_total_roles()
    )
# ---------------- ADD STAFF ----------------

@app.route('/add_staff', methods=['GET','POST'])
def add_staff():

    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        name = request.form['name']
        role = request.form['role']
        phone = request.form['phone']
        email = request.form['email']
        joining_date = request.form['joining_date']
        address = request.form['address']

        insert_staff(
            name,
            role,
            phone,
            email,
            joining_date,
            address
        )

        return redirect(url_for('staff'))

    return render_template('add_staff.html')

# ---------------- EDIT STAFF ----------------

@app.route('/edit_staff/<int:id>', methods=['GET','POST'])
def edit_staff(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    staff = get_staff(id)

    if request.method == 'POST':

        name = request.form['name']
        role = request.form['role']
        phone = request.form['phone']
        email = request.form['email']
        joining_date = request.form['joining_date']
        address = request.form['address']


        update_staff(
            id,
            name,
            role,
            phone,
            email,
            joining_date,
            address
        )

        return redirect(url_for('staff'))


    return render_template(
        'edit_staff.html',
        staff=staff
    )

# ---------------- DELETE STAFF ----------------

@app.route('/delete_staff/<int:id>')
def delete_staff_route(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    delete_staff(id)

    return redirect(url_for('staff'))



# ---------------- ADD PERSON ----------------

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():
    if 'user' not in session:
       return redirect(url_for('login'))

    if request.method == 'POST':
        name = request.form['full_name']
        alias = request.form['alias']
        age = request.form['age']
        gender = request.form['gender']
        rescue_date = request.form['rescue_date']
        location = request.form['location']
        rescued_by = request.form['rescued_by']
        status = request.form['status']
        physical_condition = request.form['physical_condition']
        medical_issues = request.form['medical_issues']
        disability = request.form['disability']
        aadhaar = request.form['aadhaar']
        family_contact = request.form['family_contact']
        remarks = request.form['remarks']

        photo = request.files['photo']
        filename = ""

        if photo and photo.filename != "":
           UPLOAD_FOLDER = os.path.join(app.root_path, "static", "images")
           os.makedirs(UPLOAD_FOLDER, exist_ok=True)

           filename = secure_filename(photo.filename)
           photo.save(os.path.join(UPLOAD_FOLDER, filename))

        insert_person(
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
            filename
        )

        return redirect(url_for('view_persons'))

    return render_template('add_person.html')


# ---------------- VIEW PERSONS ----------------

@app.route('/view_persons')
def view_persons():
    if 'user' not in session:
        return redirect(url_for('login'))

    persons = get_all_persons()

    return render_template(
        'view_persons.html',
        persons=persons
    )

# ---------------- EDIT PERSON ----------------

@app.route('/edit_person/<int:id>', methods=['GET', 'POST'])
def edit_person(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    person = get_person(id)

    if request.method == 'POST':
        name = request.form['full_name']
        alias = request.form['alias']
        age = request.form['age']
        gender = request.form['gender']
        rescue_date = request.form['rescue_date']
        location = request.form['location']
        rescued_by = request.form['rescued_by']
        status = request.form['status']
        physical_condition = request.form['physical_condition']
        medical_issues = request.form['medical_issues']
        disability = request.form['disability']
        aadhaar = request.form['aadhaar']
        family_contact = request.form['family_contact']
        remarks = request.form['remarks']

        photo = request.files.get('photo')
        
        # Kept perfectly intact with dictionary lookup matching RealDictConnection mapping
        filename = person["photo"]

        if photo and photo.filename != "":
            UPLOAD_FOLDER = os.path.join(app.root_path, "static", "images")
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)

            filename = secure_filename(photo.filename)
            photo.save(os.path.join(UPLOAD_FOLDER, filename))

        update_person(
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
            filename
        )

        return redirect(url_for('view_persons'))

    return render_template(
        'edit_person.html',
        person=person
    )


# ---------------- SEARCH ----------------

@app.route('/search', methods=['GET', 'POST'])
def search():
    if 'user' not in session:
       return redirect(url_for('login'))

    persons = []

    if request.method == 'POST':
        keyword = request.form.get('keyword')
        status = request.form.get('status')

        if keyword:
            persons = search_person(keyword)
        elif status and status != "All":
            persons = filter_by_status(status)
        else:
            persons = get_all_persons()

    return render_template(
        'search.html',
        persons=persons
    )
    

#------------------ DELETE PERSON -------------------

@app.route('/delete_person/<int:id>')
def delete_person_route(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    delete_person(id)

    return redirect(url_for('view_persons'))
    
# ---------------- ACCOUNTS ----------------

@app.route('/accounts')
def accounts():

    if 'user' not in session:
        return redirect(url_for('login'))

    volunteers = get_all_volunteers()

    return render_template(
        'accounts.html',
        volunteers=volunteers
    )


@app.route('/delete_volunteer/<int:id>')
def delete_volunteer_route(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    delete_volunteer(id)

    return redirect(url_for('accounts'))
    

# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
