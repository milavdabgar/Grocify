from flask import Blueprint, render_template, session, redirect, url_for
import sqlite3

bp = Blueprint('profile', __name__)

@bp.route('/profile')
def profile():
    # Check if the user is authenticated
    if 'email' in session:
        # Connect to the SQLite database
        cnx = sqlite3.connect('databases/fresh_basket_sample.db')
        cursor = cnx.cursor()

        # Retrieve the user data from the database
        select_query = "SELECT * FROM User WHERE Email = ?"
        cursor.execute(select_query, (session['email'],))
        user = cursor.fetchone()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        # Render the template and pass the user data to it
        cart_count = get_cart_count()
        return render_template('profile.html', user=user, cart_count=cart_count)
    else:
        return redirect(url_for('signin'))
