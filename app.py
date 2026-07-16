import os
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
    get_total_roles,

    insert_project,
    get_all_projects,
    get_project,
    update_project,
    delete_project,
    search_project,
    get_total_projects,
    get_active_projects,
    get_completed_projects,

    insert_beneficiary,
    get_all_beneficiaries,
    get_beneficiary,
    update_beneficiary,
    delete_beneficiary,
    search_beneficiary,
    get_total_beneficiaries,
    
    insert_donation,
    get_all_donations,
    get_donation,
    update_donation,
    get_total_donations,

    insert_expense,
    get_all_expenses,
    get_expense,
    update_expense,
    get_total_expenses,
    get_available_balance,

    get_total_roles
)


app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "ngo_secret_key")

from functools import wraps

def roles_required(*roles):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            if 'user' not in session:
                return redirect(url_for('login'))

            if session.get("role") not in roles:
                return render_template(
                    "access_denied.html",
                    role=session.get("role")
                )

            return f(*args, **kwargs)

        return decorated_function
    return decorator
    
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
           session['role'] = user["role"]  
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
        except Exception as e:
            # Cleaned up duplicate exception blocks from the original script
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
        volunteers=get_total_volunteers(),
        staff=get_total_staff()
    )

# ---------------- STAFF ----------------

@app.route('/staff')
@roles_required("Admin", "Staff")
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

@app.route('/add_staff', methods=['GET', 'POST'])
@roles_required("Admin", "Staff")
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

@app.route('/edit_staff/<int:id>', methods=['GET', 'POST'])
@roles_required("Admin", "Staff")
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
@roles_required("Admin", "Staff")
def delete_staff_route(id):
    if 'user' not in session:
        return redirect(url_for('login'))

    delete_staff(id)

    return redirect(url_for('staff'))

@app.route('/projects')
@roles_required("Admin", "Staff")
def projects():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template(
        'projects.html',
        projects=get_all_projects(),
        total_projects=get_total_projects(),
        active_projects=get_active_projects(),
        completed_projects=get_completed_projects()
    )

@app.route('/add_project', methods=['GET','POST'])
@roles_required("Admin", "Staff")
def add_project():

    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        insert_project(
            request.form['project_name'],
            request.form['description'],
            request.form['start_date'],
            request.form['end_date'],
            request.form['location'],
            request.form['budget'],
            request.form['status']
        )

        return redirect(url_for('projects'))

    return render_template('add_project.html')

@app.route('/edit_project/<int:id>', methods=['GET','POST'])
def edit_project(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    project = get_project(id)

    if request.method == 'POST':

        update_project(
            id,
            request.form['project_name'],
            request.form['description'],
            request.form['start_date'],
            request.form['end_date'],
            request.form['location'],
            request.form['budget'],
            request.form['status']
        )

        return redirect(url_for('projects'))

    return render_template(
        'edit_project.html',
        project=project
    )

@app.route('/delete_project/<int:id>')
def delete_project_route(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    delete_project(id)

    return redirect(url_for('projects'))

@app.route('/search_projects', methods=['POST'])
def search_projects():

    if 'user' not in session:
        return redirect(url_for('login'))

    keyword = request.form['keyword']

    projects = search_project(keyword)

    return render_template(
        'projects.html',
        projects=projects,
        total_projects=get_total_projects(),
        active_projects=get_active_projects(),
        completed_projects=get_completed_projects()
    )

@app.route('/beneficiaries')
@roles_required("Admin", "Staff")
def beneficiaries():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template(
        'beneficiaries.html',
        beneficiaries=get_all_beneficiaries(),
        total_beneficiaries=get_total_beneficiaries()
    )

@app.route('/add_beneficiary', methods=['GET','POST'])
def add_beneficiary():

    if 'user' not in session:
        return redirect(url_for('login'))

    if request.method == 'POST':

        insert_beneficiary(
            request.form['beneficiary_name'],
            request.form['age'],
            request.form['gender'],
            request.form['phone'],
            request.form['address'],
            request.form['project_name'],
            request.form['support_type'],
            request.form['registration_date']
        )

        return redirect(url_for('beneficiaries'))

    return render_template('add_beneficiary.html')

@app.route('/edit_beneficiary/<int:id>', methods=['GET','POST'])
def edit_beneficiary(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    beneficiary = get_beneficiary(id)

    if request.method == 'POST':

        update_beneficiary(
            id,
            request.form['beneficiary_name'],
            request.form['age'],
            request.form['gender'],
            request.form['phone'],
            request.form['address'],
            request.form['project_name'],
            request.form['support_type'],
            request.form['registration_date']
        )

        return redirect(url_for('beneficiaries'))

    return render_template(
        'edit_beneficiary.html',
        beneficiary=beneficiary
    )

@app.route('/delete_beneficiary/<int:id>')
def delete_beneficiary_route(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    delete_beneficiary(id)

    return redirect(url_for('beneficiaries'))

@app.route('/search_beneficiaries', methods=['POST'])
def search_beneficiaries():

    if 'user' not in session:
        return redirect(url_for('login'))

    keyword = request.form['keyword']

    beneficiaries = search_beneficiary(keyword)

    return render_template(
        'beneficiaries.html',
        beneficiaries=beneficiaries,
        total_beneficiaries=get_total_beneficiaries()
    )
    
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
@roles_required("Admin", "Staff")
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

# ---------------- FINANCE ----------------

@app.route('/finance')
def finance():

    if 'user' not in session:
        return redirect(url_for('login'))

    donations = get_all_donations()
    expenses = get_all_expenses()

    return render_template(
        'finance.html',
        donations=donations,
        expenses=expenses,
        total_donations=get_total_donations(),
        total_expenses=get_total_expenses(),
        balance=get_available_balance()
    )


# ---------------- ADD DONATION ----------------

@app.route('/add_donation', methods=['POST'])
def add_donation():

    if 'user' not in session:
        return redirect(url_for('login'))

    donor_name = request.form['donor_name']
    donation_type = request.form['donation_type']
    amount = request.form['amount']
    donated_on = request.form['donated_on']
    remarks = request.form['remarks']


    insert_donation(
        donor_name,
        donation_type,
        amount,
        donated_on,
        remarks
    )

    return redirect(url_for('finance'))

# ---------------- EDIT DONATION ----------------

@app.route('/edit_donation/<int:id>', methods=['GET', 'POST'])
def edit_donation(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    donation = get_donation(id)

    if request.method == 'POST':

        donor_name = request.form['donor_name']
        donation_type = request.form['donation_type']
        amount = request.form['amount']
        donated_on = request.form['donated_on']
        remarks = request.form['remarks']

        update_donation(
            id,
            donor_name,
            donation_type,
            amount,
            donated_on,
            remarks
        )

        return redirect(url_for('finance'))

    return render_template(
        'edit_donation.html',
        donation=donation
    )

# ---------------- ADD EXPENSE ----------------

@app.route('/add_expense', methods=['POST'])
def add_expense():

    if 'user' not in session:
        return redirect(url_for('login'))

    purpose = request.form['purpose']
    amount = request.form['amount']
    spent_on = request.form['spent_on']
    paid_to = request.form['paid_to']
    remarks = request.form['remarks']


    insert_expense(
        purpose,
        amount,
        spent_on,
        paid_to,
        remarks
    )

    return redirect(url_for('finance'))

# ---------------- EDIT EXPENSE ----------------

@app.route('/edit_expense/<int:id>', methods=['GET', 'POST'])
def edit_expense(id):

    if 'user' not in session:
        return redirect(url_for('login'))

    expense = get_expense(id)

    if request.method == 'POST':

        purpose = request.form['purpose']
        amount = request.form['amount']
        spent_on = request.form['spent_on']
        paid_to = request.form['paid_to']
        remarks = request.form['remarks']

        update_expense(
            id,
            purpose,
            amount,
            spent_on,
            paid_to,
            remarks
        )

        return redirect(url_for('finance'))

    return render_template(
        'edit_expense.html',
        expense=expense
    )
    
# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():
    session.pop('user', None)
    session.pop('role', None)
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
