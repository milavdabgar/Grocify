from flask import Blueprint, request, render_template, redirect, url_for
from controllers import get_cart_count
from models import Product
from extensions import db

bp = Blueprint('search', __name__)

@bp.route('/search')
def search():
    # Get the search query from the request's query parameters
    query = request.args.get('query')

    # Check if the query is None or empty
    if not query or query.strip() == '':
        # Handle the case when no query is provided
        return redirect(url_for('products.products'))
   
    # Search for products matching the query and retrieve them as tuples
    product_columns = [getattr(Product, column_name) for column_name in Product.__table__.columns.keys()]   
    products = db.session.query(*product_columns).filter(
        db.or_(Product.name.ilike(f'%{query}%'), Product.description.ilike(f'%{query}%'))
    ).all()

    # checks items on the cart
    cart_count = get_cart_count()

    # Render the template and pass the product data to it
    return render_template('search_results.html', products=products, query=query, cart_count=cart_count)

