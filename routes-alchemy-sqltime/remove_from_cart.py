from flask import Blueprint, request, session, redirect, url_for
from models import User, Cart, CartProduct
from extensions import db

bp = Blueprint('remove_from_cart', __name__)

@bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('signin.signin'))

    # Get the product ID from the request form
    product_id = request.form.get('product_id')

    # Retrieve the user's cart ID
    user = User.query.filter_by(email=session['email']).first()
    cart_id = Cart.query.filter_by(user_id=user.id).first().id

    # Delete the product from the user's cart
    CartProduct.query.filter_by(cart_id=cart_id, product_id=product_id).delete()

    # Commit the changes
    db.session.commit()

    # Redirect back to the cart page
    return redirect(url_for('cart.cart'))
