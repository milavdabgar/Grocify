from flask import Blueprint, render_template, session, redirect, url_for, request
import sqlite3

bp = Blueprint('search', __name__)

@bp.route('/search')
def search():
    # Get the search query from the request's query parameters
    query = request.args.get('query')

    # Check if the query is None or empty
    if not query or query.strip() == '':
        # Handle the case when no query is provided
        return redirect(url_for('products'))

    # Connect to the SQLite database
    cnx = sqlite3.connect('databases/fresh_basket_sample.db')
    cursor = cnx.cursor()

    # Search for products matching the query
    search_query = "SELECT * FROM Product WHERE Name LIKE ? OR Description LIKE ?"
    pattern = f'%{query}%'
    cursor.execute(search_query, (pattern, pattern))
    products = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # checks items on the cart
    cart_count = get_cart_count()

    # Render the template and pass the product data to it
    return render_template('search_results.html', products=products, query=query, cart_count=cart_count)
