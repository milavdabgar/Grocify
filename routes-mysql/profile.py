from flask import Blueprint, render_template, session, redirect, url_for
import mysql.connector
from config import db_config
from controllers import get_cart_count

bp = Blueprint('profile', __name__)

@bp.route('/profile')
def profile():
    # Check if the user is authenticated (session exists)
    if 'email' in session:
        # Connect to the MySQL database
        cnx = mysql.connector.connect(**db_config)
        cursor = cnx.cursor()

        # Retrieve user data from the database
        cursor.execute("SELECT * FROM User WHERE Email = %s", (session['email'],))
        user = cursor.fetchone()

         # Retrieve shipping info from database
        select_shipping_query = """
        SELECT * FROM Shipping
        INNER JOIN User ON Shipping.UserId = User.Id
        WHERE User.Email = %s
        """
        cursor.execute(select_shipping_query, (session['email'],))
        shipping_info = cursor.fetchall()

        # Close the cursor and connection
        cursor.close()
        cnx.close()

        # checks items on the cart
        cart_count = get_cart_count()

        # Render the template and pass the user data to it
        return render_template('profile.html', user=user, shipping_info=shipping_info, cart_count=cart_count)
    else:
        return redirect(url_for('signin.signin'))