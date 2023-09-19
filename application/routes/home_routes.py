from flask import Blueprint, render_template, session, redirect, url_for
from application.routes.cart_routes import get_cart_count

bp = Blueprint('home_routes', __name__)

@bp.route('/')
def landing():
    # return  render_template('home_landing.html')
    return  render_template('home_landing.html')

@bp.route('/dashboard')
def dashboard():
    # Check if the user is authenticated
    if 'email' in session:
        if session['email'] == 'admin@grocify.com':
            return redirect(url_for('home_routes.admin_panel'))
        else:
            # Retrieve the cart count using SQLAlchemy
            cart_count = get_cart_count()
            return render_template('home_dashboard.html', cart_count=cart_count)
    else:
        return redirect(url_for('auth_routes.signin'))

@bp.route('/admin', methods=['GET'])
def admin_panel():
    # Check if the user is authenticated as an admin
    if 'email' in session and session['email'] == 'admin@grocify.com':
        return render_template('home_admin.html')
    else:
        return redirect(url_for('auth_routes.signin'))


