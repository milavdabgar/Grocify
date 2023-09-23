from flask import Blueprint, render_template, session, redirect, url_for
from app.routes.cart_routes import get_cart_count

bp = Blueprint('home_routes', __name__)

@bp.route('/')
def landing():
    images = ["images/banner1.jpg", "images/banner2.jpg", "images/banner3.jpg", "images/banner4.jpg", "images/banner5.jpg"]
    return  render_template('home/home_landing.html', images=images)

@bp.route('/dashboard')
def dashboard():
    # Check if the user is authenticated
    if 'email' in session:
        if session['email'] == 'admin@grocify.com':
            return redirect(url_for('home_routes.admin_panel'))
        else:
            # Retrieve the cart count using SQLAlchemy
            cart_count = get_cart_count()
            return render_template('home/home_dashboard.html', cart_count=cart_count)
    else:
        return redirect(url_for('auth.login'))

@bp.route('/admin', methods=['GET'])
def admin_panel():
    # Check if the user is authenticated as an admin
    if 'email' in session and session['email'] == 'admin@grocify.com':
        return render_template('home/home_admin.html')
    else:
        return redirect(url_for('auth.login'))
