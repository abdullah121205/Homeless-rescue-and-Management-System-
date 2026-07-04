from flask import Flask, render_template, request, redirect, url_for, session

from db import (
    insert_user,
    login_user,
    insert_person,
    get_all_persons,
    search_person,
    filter_by_status,
    delete_person
)

app = Flask(__name__)
app.secret_key = "ngo_secret_key"


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

        insert_user(fullname, username, email, password)

        return redirect(url_for('login'))

    return render_template('register.html')


# ---------------- DASHBOARD ----------------

@app.route('/dashboard')
def dashboard():

    if 'user' not in session:
        return redirect(url_for('login'))

    return render_template('dashboard.html')


# ---------------- ADD PERSON ----------------

@app.route('/add_person', methods=['GET', 'POST'])
def add_person():

    if request.method == 'POST':

        name = request.form['full_name']
        age = request.form['age']
        gender = request.form['gender']
        location = request.form['location']
        status = request.form['status']

        insert_person(name, age, gender, location, status)

        return redirect(url_for('view_persons'))

    return render_template('add_person.html')


# ---------------- VIEW PERSONS ----------------

@app.route('/view_persons')
def view_persons():

    persons = get_all_persons()

    return render_template(
        'view_persons.html',
        persons=persons
    )


# ---------------- SEARCH ----------------

@app.route('/search', methods=['GET', 'POST'])
def search():

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
    
#------------------ Delete Person -------------------

@app.route('/delete_person/<int:id>')
def delete_person_route(id):

    delete_person(id)

    return redirect(url_for('view_persons'))
    
# ---------------- LOGOUT ----------------

@app.route('/logout')
def logout():

    session.pop('user', None)

    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(debug=True)
