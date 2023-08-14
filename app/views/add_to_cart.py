from flask import Blueprint, request, session, redirect, url_for, jsonify
from app.models import Cart, User, CartProduct
from app.extensions import db

add_to_cart_bp = Blueprint('add_to_cart', __name__)

@add_to_cart_bp.route('/add_to_cart', methods=['POST'])
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

# from flask import Blueprint, request, session, redirect, url_for
# from app.models import Cart, User, CartProduct
# from app.extensions import db

# add_to_cart_bp = Blueprint('add_to_cart', __name__)

# @add_to_cart_bp.route('/add_to_cart', methods=['POST'])
# def add_to_cart():
#     if 'email' not in session:
#         return redirect(url_for('signin.signin'))

#     product_id = request.form.get('product_id')

#     user = User.query.filter_by(email=session['email']).first()
#     cart = get_active_cart(user)

#     cart_product_id = insert_product_into_cart(cart, product_id)

#     return {'status': 'success'}


# def get_active_cart(user):
#     cart = Cart.query.filter_by(user_id=user.id).first()

#     if not cart:
#         cart = Cart(user_id=user.id)
#         db.session.add(cart)
#         db.session.commit()

#     return cart


# def insert_product_into_cart(cart, product_id):
#     cart_product = CartProduct(cart_id=cart.id, product_id=product_id)
#     db.session.add(cart_product)
#     db.session.commit()

#     return cart_product.id
