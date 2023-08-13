from flask import Blueprint, render_template, session, redirect, url_for
from controllers import get_cart_count
from extensions import db
from models import User, Shipping

bp = Blueprint('profile', __name__)

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

        # Render the template and pass the user data to it
        return render_template('profile.html', user=user, shipping_info=shipping_info, cart_count=cart_count)
    else:
        return redirect(url_for('signin.signin'))
