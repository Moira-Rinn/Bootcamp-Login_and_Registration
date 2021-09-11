from flask import render_template, redirect, request, session, flash
from Flask_App import app
from Flask_App.models.user import User
from Flask_App.models.login import Login
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


@app.route('/')
def index():
    query = "SELECT * FROM users;"
    users = User.get_all(query)
    return render_template("index.html", all_users=users)


@app.route('/create/user', methods=['POST'])
def create_user():
    uData = {
        "fname": request.form['fname'],
        "lname": request.form['lname'],
        "email": request.form['email']
    }

    pw1_hash = bcrypt.generate_password_hash(request.form['pass1'])
    pw2_hash = bcrypt.generate_password_hash(request.form['pass2'])

    pData = {
        "pass1": pw1_hash,
        "pass2": pw2_hash
    }

    if not User.registration_validation(request.form) or not Login.password_validation(request.form):
        return redirect('/')
    new_user = User.save(uData)
    session['user_name'] = request.form['fname']
    pData['user_id'] = new_user
    Login.save(pData)

    return redirect(f'/show/{new_user}')


@app.route('/show/<int:user_id>')
def welcome(user_id):
    if session == {}:
        return redirect('/')
    return render_template('welcome.html')


@app.route('/logout')
def loggedout():
    session.clear()
    return redirect("/")


@app.route('/login', methods=['POST'])
def login():
    uQuery = 'SELECT * FROM users WHERE email = %(email)s;'
    uData = {'email': request.form['email']}
    user_in_db = User.get_all(uQuery, uData)
    user_id = user_in_db[0].id

    lQuery = "SELECT * FROM logins WHERE user_id = %(user_id)s;"
    lData = {'user_id': user_id}
    user_password = Login.get_all(lQuery, lData)

    if not user_in_db or not user_password:
        flash("Invalid Email/Password")
        return redirect("/")
    if not bcrypt.check_password_hash(user_password[0].pass1, request.form['pass']):
        flash("Invalid Email/Password")
        return redirect('/')
    session['user_name'] = user_in_db[0].first_name
    return redirect(f"/show/{user_in_db[0].id}")
    # return render_template('test.html')


# @app.route('/dashboard')
# def dash(user_id):
#     return render_template("")

# @app.route('/users')
# def user():
#     query = "SELECT * FROM users;"
#     users = User.get_all(query)
#     return render_template("results.html", all_users=users)

# @app.route('/edit_page/<int:user_id>')
# def edit_page(user_id):
#     query = "SELECT * FROM users WHERE id = %(id)s;"
#     data = {
#         'id': user_id
#     }
#     user = User.get_all(query, data)
#     print(user)
#     return render_template("edit_page.html", user=user[0])


# @app.route('/update/<int:user_id>', methods=['POST'])
# def update(user_id):
#     query = "UPDATE users SET first_name=%(fname)s, last_name=%(lname)s, email=%(email)s, updated_at = NOW() WHERE id = %(id)s;"
#     data = {
#         'id': user_id,
#         "fname": request.form['fname'],
#         "lname": request.form['lname'],
#         "email": request.form['email']
#     }
#     user = User.edit_user(query, data)
#     print(user)
#     return redirect(f"/show/{user_id}")


# @app.route('/delete/<int:user_id>')
# def remove_user(user_id):
#     query = "DELETE FROM users WHERE id = %(id)s;"
#     data = {
#         'id': user_id,
#     }
#     User.remove_user(query, data)
#     return redirect('/users')
