from flask import session, current_app
from app.models import *

def get_cart_count():
    # Check if the user is authenticated
    if 'email' in session:
        # Retrieve the cart count for the user
        cart_count = CartProduct.query \
            .join(Cart) \
            .join(User) \
            .filter(User.email == session['email']) \
            .count()

        # Log the cart count
        current_app.logger.info(f"Cart count: {cart_count}")

        return cart_count

    pass
