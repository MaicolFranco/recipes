from flask import  render_template, request, redirect, url_for, flash, session
from flask_app import app
from flask_app.models.user import User
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['POST'])
def register():
    validation = User.validate_registration(request.form)
    if validation:
        pwd = bcrypt.generate_password_hash(request.form['password'])
        form = {
            'first_name': request.form['first_name'],
            'last_name':request.form['last_name'],
            'email':request.form['email'],
            'password': pwd
            }
        session['user_id']= User.register(form)
        return redirect(url_for('recipes'))
    else:
        return redirect(url_for('index'))

@app.route('/login', methods=['POST'])
def login():
    user= User.get_by_email(request.form)
    if not user:
        flash('Invalid email','login_error')
        return redirect(url_for('index'))
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid password','login_error')
        return redirect(url_for('index'))
    session['user_id'] = user.id
    return redirect(url_for('recipes'))

@app.route('/logout')
def logout():
        session.clear()
        return redirect(url_for('index'))