from flask import Blueprint, request, session, redirect, url_for, jsonify
from models import Cart, User, CartProduct
from extensions import db

bp = Blueprint('add_to_cart', __name__)

@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'email' not in session:
        return redirect(url_for('signin.signin'))

    # Retrieve the product ID from the request form
    product_id = request.form.get('product_id')

    # Retrieve the user's cart
    user = User.query.filter_by(email=session['email']).first()
    cart = Cart.query.filter_by(user_id=user.id).first()

    # Check if the user has an active cart
    if cart:
        cart_id = cart.id
    else:
        # If the user does not have a cart, create a new cart
        cart = Cart(user_id=user.id)
        db.session.add(cart)
        db.session.commit()

        # Retrieve the new cart ID
        cart_id = cart.id

    # Insert the product into the user's cart
    cart_product = CartProduct(cart_id=cart_id, product_id=product_id)
    db.session.add(cart_product)
    db.session.commit()

    # Redirect back to the products page
    return jsonify({'status': 'success'})
