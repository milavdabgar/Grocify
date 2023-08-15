from flask import Blueprint, render_template, request, session, redirect, url_for, jsonify
from app.extensions import db
from app.models import User, Cart, CartProduct, Product, Shipping

bp = Blueprint('cart_routes', __name__)

@bp.route('/')
def get_cart_count():
    # Check if the user is authenticated
    if session.get('email'):
        try:
            # Retrieve the cart count for the user
            count = CartProduct.query \
                .join(Cart) \
                .join(User) \
                .filter(User.email == session['email']) \
                .count()

            return count
        except Exception as e:
            # Handle any exceptions that may occur
            # Log the exception using app.logger
            print("Error retrieving cart count")
            return None

    return None

@bp.route('/cart')
def cart():
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('auth_routes.signin'))

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

    # Render the template and pass the cart data and shipping information to it
    return render_template('cart.html', cart_products=cart_products, total_price=total_price, shipping_info=shipping_info)

@bp.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    if 'email' not in session:
        return redirect(url_for('auth_routes.signin'))

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
    
@bp.route('/remove_from_cart', methods=['POST'])
def remove_from_cart():
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('auth_routes.signin'))

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
    return redirect(url_for('cart_routes.cart'))
