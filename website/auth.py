from flask import Blueprint, render_template, request
from flask import url_for, redirect, session
from database import add_user, check_user, check_user_for_login, check_email, authenticate_user
from hash_text import encrypt_string
from website import add_flash_message
from email_verify import is_valid_email

auth = Blueprint('auth', __name__)

# define a route for the signup form and form submission
@auth.route('/signup', methods=['GET','POST'])
def signin_page():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            passwd = request.form['password']
            encrypted_passd = encrypt_string(passwd)

            # Check if the username is already taken
            if check_user(name):
                add_flash_message('Username is already taken', category='error')
                return redirect(url_for('auth.signin_page'))

            # Check if the email is already registered
            if check_email(email):
                add_flash_message('Email is already registered', category='error')
                return redirect(url_for('auth.signin_page'))

            # Validate the email format
            if not is_valid_email(email):
                add_flash_message('Invalid email format', category='error')
                return redirect(url_for('auth.signin_page'))

            # Ensure the password is at least 6 characters long
            if len(passwd) < 6:
                add_flash_message('Password must be at least 6 characters long', category='error')
                return redirect(url_for('auth.signin_page'))

            # Add the user to the database
            add_user(name, email, encrypted_passd)

            # Authenticate the user and get user_id
            logged_in = authenticate_user(name, encrypted_passd)
            session['logged_in'] = logged_in

            add_flash_message('Account created successfully', category='success')
            print(f'Account created for user_id: {logged_in}')
            return redirect(url_for('views.home'))

        
        except Exception as e:
            # handle other exceptions
            add_flash_message(f'Error: {e}', category='error')
            return redirect(url_for('auth.signup_page'))
    else:
        # display the registration form
        return render_template('signup.html')
       

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        passwd = request.form['password']
        encrypted_passd = encrypt_string(passwd)

        if check_user_for_login(name, encrypted_passd):
            # Set session variable to indicate that the user is logged in
            logged_in = authenticate_user(name, encrypted_passd)
            session['logged_in'] = logged_in
            print("Login successful. Redirecting to home.")
            return redirect(url_for('views.home'))
        else:
            add_flash_message('Incorrect login', category='error')
            print("Login failed. Redirecting to login.")
            return redirect(url_for('auth.login'))
        
    else:
        return render_template('login.html')
    
@auth.route('/logout')
def logout():
    # Clear the session variable upon logout
    session.pop('logged_in', None)
    add_flash_message('Logged out successfully.', category='success')
    return redirect(url_for('views.home'))