from flask import Blueprint, session, redirect, url_for
from app.extensions import db
from app.models import User, Cart, Order, OrderProduct, Product, CartProduct

bp = Blueprint('place_order', __name__)

@bp.route('/place_order', methods=['POST'])
def place_order():
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('signin.signin'))

    # Retrieve the user's ID
    user_id = db.session.query(User.id).filter(User.email == session['email']).scalar()

    # Retrieve the user's cart ID
    cart_id = db.session.query(Cart.id).filter(Cart.user_id == user_id).scalar()

    # Calculate the total price of the order
    total_price = db.session.query(db.func.sum(Product.price)).join(CartProduct).filter(CartProduct.cart_id == cart_id).scalar()

    # Insert the order into the database
    order = Order(user_id=user_id, status='processing', total=total_price)
    db.session.add(order)
    db.session.commit()

    # Retrieve the products from the user's cart
    cart_products = db.session.query(CartProduct.product_id).filter(CartProduct.cart_id == cart_id).all()
    order_products = [(order.id, product_id) for product_id, in cart_products]

    # Insert the products into the OrderProduct table
    for order_product in order_products:
        order_product = OrderProduct(order_id=order_product[0], product_id=order_product[1])
        db.session.add(order_product)

    db.session.commit()

    # Remove the products from the user's cart
    db.session.query(CartProduct).filter(CartProduct.cart_id == cart_id).delete()
    db.session.commit()

    # Redirect to the order confirmation page
    return redirect(url_for('order_confirmation.order_confirmation', order_id=order.id))