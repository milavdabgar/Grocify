from flask import Blueprint, render_template, session, redirect, url_for
from extensions import db
from models import User, Cart, CartProduct, Product, Shipping

bp = Blueprint('cart', __name__)

@bp.route('/cart')
def cart():
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('signin.signin'))

    # Retrieve cart data for the user from the database 
    cart_products = db.session.query(Product.id, Product.name, Product.description, Product.price, Product.image, Product.category) \
        .join(CartProduct, CartProduct.product_id == Product.id) \
        .join(Cart, CartProduct.cart_id == Cart.id) \
        .join(User, Cart.user_id == User.id) \
        .filter(User.email == session['email']) \
        .all()

    cart_product_tuples = [tuple(item) for item in cart_products]

    # Calculate the total price of the cart
    total_price = db.session.query(db.func.sum(Product.price))\
        .join(CartProduct, Product.id == CartProduct.product_id)\
        .join(Cart, CartProduct.cart_id == Cart.id)\
        .join(User, Cart.user_id == User.id)\
        .filter(User.email == session['email'])\
        .scalar()

    shipping_columns = [getattr(Shipping, column_name) for column_name in Shipping.__table__.columns.keys()]   
    shipping_info = db.session.query(*shipping_columns).join(User).filter(
        User.email == session['email']
    ).all()

    # Render the template and pass the cart data and shipping information to it
    return render_template('cart.html', cart_products=cart_product_tuples, total_price=total_price, shipping_info=shipping_info)