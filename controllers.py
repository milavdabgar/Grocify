from flask import session
from models import *

def get_cart_count():
    # Check if the user is authenticated
    if 'email' in session:
        # Retrieve the cart count for the user
        cart_count = CartProduct.query \
            .join(Cart) \
            .join(User) \
            .filter(User.email == session['email']) \
            .count()
        return cart_count

    pass
