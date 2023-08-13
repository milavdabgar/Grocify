from flask import session, current_app as app
from app.models import CartProduct, Cart, User

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
            app.logger.exception("Error retrieving cart count")
            return None

    return None
