from flask import Blueprint, render_template, request, session, redirect, url_for
import bcrypt
from extensions import db
from models import User

bp = Blueprint('signin', __name__)

@bp.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        # Retrieve form data
        email = request.form.get('email')
        password = request.form.get('password')

        # Retrieve the user from the database
        user = User.query.filter_by(email=email).first()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user.password.encode('utf-8')):
            # If credentials are valid, create a session for the user
            session['email'] = email

            # Redirect to the home page
            return redirect(url_for('home.home'))

        # User not found or invalid credentials
        return render_template('signup.html')

    # If it's a GET request and the user is already signed in, redirect to the home page
    if 'email' in session:
        return redirect(url_for('home.home'))

    # If it's a GET request and the user is not signed in, render the sign-in page
    return render_template('signin.html')
