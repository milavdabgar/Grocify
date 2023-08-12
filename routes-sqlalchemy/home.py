from flask import Blueprint, render_template, session, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from ..databases.models import CartProduct, Cart, User

db = SQLAlchemy()

bp = Blueprint('home', __name__)

@bp.route('/home')
def home():
    # Check if the user is authenticated
    if 'email' in session:
        if session['email'] == 'admin@frb.com':
            return redirect(url_for('admin_panel.admin_panel'))
        else:
            # For regular users, continue with the existing functionality
            cart_count = get_cart_count(session['email'])
            return render_template('index.html', cart_count=cart_count)
    else:
        return redirect(url_for('signin.signin'))

def get_cart_count(email):
    # Retrieve the cart count for the user
    cart_count = db.session.query(db.func.count(CartProduct.ProductId)).\
        join(Cart, CartProduct.CartId == Cart.Id).\
        join(User, Cart.UserId == User.Id).\
        filter(User.Email == email).\
        scalar()

    return cart_count
