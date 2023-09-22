from flask import Blueprint, render_template, request, session, redirect, url_for
import bcrypt
from app import db
from app.models import User, Shipping
from app.routes.cart_routes import get_cart_count

bp = Blueprint('auth_routes', __name__)

@bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Retrieve form data
        name = request.form.get('name')
        email = request.form.get('email')
        password = request.form.get('password')
        phone = request.form.get('phone')

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        # Check if the email already exists in the database
        existing_user = User.query.filter_by(email=email).first()

        if existing_user:
            # If the email already exists, display an error message
            error_message = 'Email already exists. Please choose a different email.'
            return render_template('auth2/auth_sigup.html', error_message=error_message)
        else:
            # Insert the user data into the database
            new_user = User(name=name, email=email, password=hashed_password, phone=phone)
            db.session.add(new_user)
            db.session.commit()

        # Create a session for the user
        session['email'] = email

        # Redirect to the profile page
        return redirect(url_for('auth_routes.profile'))
    else:
        return render_template('auth2/auth_sigup.html')

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
            return redirect(url_for('home_routes.dashboard'))

        # User not found or invalid credentials
        return render_template('auth2/auth_sigup.html')

    # If it's a GET request and the user is already signed in, redirect to the home page
    if 'email' in session:
        return redirect(url_for('home_routes.dashboard'))

    # If it's a GET request and the user is not signed in, render the sign-in page
    return render_template('auth2/auth_sigin.html')

@bp.route('/signout')
def signout():
    # Clear the session
    session.clear()

    # Redirect to the sign-in page
    return redirect(url_for('auth_routes.signin'))

@bp.route('/profile')
def profile():
    # Check if the user is authenticated (session exists)
    if 'email' in session:
        # Retrieve user data from the database
        user_columns = [getattr(User, column_name) for column_name in User.__table__.columns.keys()] 
        user = db.session.query(*user_columns).filter(User.email == session['email']).first()
        # user = User.query.filter_by(email=session['email']).first()
        
        # Retrieve shipping info from database
        shipping_columns = [getattr(Shipping, column_name) for column_name in Shipping.__table__.columns.keys()]   
        shipping_info = db.session.query(*shipping_columns).join(User).filter(
            User.email == session['email']
        ).all()
                
        # checks items on the cart
        cart_count = get_cart_count()
        
        if session['email'] == 'admin@grocify.com':
            return render_template('auth2/auth_profile_admin.html', user=user, shipping_info=shipping_info, cart_count=cart_count)
        else:
            # Render the template and pass the user data to it
            return render_template('auth2/auth_profile.html', user=user, shipping_info=shipping_info, cart_count=cart_count)
    else:
        return redirect(url_for('auth_routes.signin'))