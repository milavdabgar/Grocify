from flask import Blueprint, render_template, request, session, redirect, url_for
from app import db
from app.models import User, Order, OrderProduct, Product, Shipping, Cart, CartProduct
from app.routes.cart_routes import get_cart_count

bp = Blueprint('order_routes', __name__)

@bp.route('/shipping', methods=['GET', 'POST'])
def shipping():
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        if 'delete_shipping' in request.form:
            # Delete shipping information
            shipping_id = request.form.get('delete_shipping')
            # Delete the shipping information from the database
            Shipping.query.filter_by(id=shipping_id).delete()
            db.session.commit()
            # Redirect the user back to the shipping page
            return redirect(url_for('order_routes.shipping'))

        else:
            # Retrieve shipping information from the form
            full_name = request.form.get('full_name')
            street_address = request.form.get('street_address')
            city = request.form.get('city')
            state_province = request.form.get('state_province')
            postal_code = request.form.get('postal_code')
            country = request.form.get('country')

            # Retrieve the user's ID
            user = User.query.filter_by(email=session['email']).first()

            # Insert the shipping information into the shipping table
            shipping = Shipping(user_id=user.id, full_name=full_name, street_address=street_address,
                                city=city, state_province=state_province, postal_code=postal_code, country=country)
            db.session.add(shipping)
            db.session.commit()

            # Retrieve shipping info from database
            shipping_columns = [getattr(Shipping, column_name) for column_name in Shipping.__table__.columns.keys()]   
            shipping_info = db.session.query(*shipping_columns).join(User).filter(
                User.email == session['email']
            ).all()

            # redirect the user back to the shipping page
            return render_template('order/order_shipping.html', shipping_info=shipping_info)

    # If it's a GET request, render the shipping information form
    # Retrieve shipping info from database
    shipping_columns = [getattr(Shipping, column_name) for column_name in Shipping.__table__.columns.keys()]   
    shipping_info = db.session.query(*shipping_columns).join(User).filter(
        User.email == session['email']
    ).all()

    return render_template('order/order_shipping.html', shipping_info=shipping_info)

@bp.route('/checkout', methods=['GET', 'POST'])
def checkout():
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('auth.login'))

    # Retrieve cart data for the user from the database
    # Retrieve cart data for the user from the database 
    cart_products = db.session.query(Product.id, Product.name, Product.description, Product.price, Product.image, Product.category) \
        .join(CartProduct, CartProduct.product_id == Product.id) \
        .join(Cart, CartProduct.cart_id == Cart.id) \
        .join(User, Cart.user_id == User.id) \
        .filter(User.email == session['email']) \
        .all()

    # cart_product_tuples = [tuple(item) for item in cart_products]

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
    
    # Render the template and pass the cart data to it
    return render_template('order/order_checkout.html',
                           cart_products=cart_products,
                           total_price=total_price,
                           shipping_info=shipping_info)

@bp.route('/place_order', methods=['POST'])
def place_order():
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('auth.login'))

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
    return redirect(url_for('order_routes.order_confirmation', order_id=order.id))

@bp.route('/order_confirmation/<int:order_id>')
def order_confirmation(order_id):
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('auth.login'))

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
    return render_template('order/order_confirmation.html',
                           order_id=order_id,
                           order_products=order_products,
                           total_price=total_price,
                           shipping_info=shipping_info,
                           cart_count=cart_count)
