from flask import Blueprint, render_template
import sqlite3

bp = Blueprint('products', __name__)

@bp.route('/products')
def products():
    # Connect to the MySQL database
    cnx = sqlite3.connect('databases/fresh_basket_sample.db')
    cursor = cnx.cursor()

    # Retrieve product data from the database
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Render the template and pass the product data to it
    cart_count = get_cart_count()
    return render_template('shop.html', products=products, cart_count=cart_count)
