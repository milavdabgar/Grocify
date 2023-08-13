from flask import Blueprint, render_template, session, redirect, url_for
from app.extensions import db
from app.models import User, Order, OrderProduct, Product, Shipping
from app.controllers import get_cart_count

bp = Blueprint('order_confirmation', __name__)

@bp.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('signin.signin'))

    # Retrieve the order details using Flask SQLAlchemy
    order_products = db.session.query(
        Order.id, Product.name, Product.description, Product.price,
        Product.image, Product.category
    ).join(OrderProduct, Order.id == OrderProduct.order_id).join(
        Product, OrderProduct.product_id == Product.id
    ).join(User, Order.user_id == User.id).filter(
        User.email == session['email'], Order.id == order_id
    ).all()

    # Calculate the total price of the order
    total_price = db.session.query(db.func.sum(Product.price)).\
        join(OrderProduct, OrderProduct.product_id == Product.id).\
        join(Order, Order.id == OrderProduct.order_id).\
        join(User, User.id == Order.user_id).\
        filter(User.email == session['email']).\
        filter(Order.id == order_id).\
        scalar()
    
    # Retrieve shipping info from database
    shipping_columns = [getattr(Shipping, column_name) for column_name in Shipping.__table__.columns.keys()]   
    shipping_info = db.session.query(*shipping_columns).join(User).filter(
        User.email == session['email']
    ).all()
    
    # Close the session
    db.session.close()

    # checks items on the cart
    cart_count = get_cart_count()

    # Convert the query results to a list of tuples
    order_products = [tuple(row) for row in order_products]

    # Render the template and pass the order data to it
    return render_template('order_confirmation.html',
                           order_id=order_id,
                           order_products=order_products,
                           total_price=total_price,
                           shipping_info=shipping_info,
                           cart_count=cart_count)
