from flask import Blueprint, render_template, request, flash
from database import add_user, check_user
from hash_text import encrypt_string

auth = Blueprint('auth', __name__)

# define a route for the signup form and form submission
@auth.route('/signup', methods=['GET','POST'])
def registration_submit():
    if request.method == 'POST':
        try:
            name = request.form['name']
            email = request.form['email']
            passwd = request.form['password']
            encrypted_passd = encrypt_string(passwd)

            #check if the user being registered is in the system
            if not check_user(name, encrypted_passd):
                # add the user the to the database
                add_user(name, email, encrypted_passd)
            else:
                flash('User already has an account', category='error')
            
            # redirect to a thank you page
            return 'thank you'
        
        except Exception as e:
            # handle other exceptions
            return f'Something went wrong: {str(e)}'
    else:
        # display the registration form
        return render_template('signup.html')
       

@auth.route('/login', methods=['GET','POST'])
def login():
    if request.method == 'POST':
        name = request.form['name']
        passwd = request.form['password']
        encrypted_passd = encrypt_string(passwd)

        if check_user(name, encrypted_passd):
            return 'In the system'
        else:
            #flash('Username taken', category='error')
            return 'Not In the system'
        
    else:
        return render_template('login.html')
    
@auth.route('/logout')
def logout():
    return 'logout'