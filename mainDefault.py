from flask import Flask, render_template, request, session, redirect, url_for, jsonify
from routes import landing, home, recipe, products, signup, signin, profile, signout, search, cart, add_to_cart, remove_from_cart, checkout, place_order, order_confirmation, shipping, videos, admin_panel
import os
from config import *


app = Flask(__name__)
app.secret_key = os.environ.get('APP_SECRET_KEY')

# app.register_blueprint(landing.bp, url_prefix='/')
# app.register_blueprint(home.bp, url_prefix='/home')
# app.register_blueprint(recipe.bp, url_prefix='/recipe')
# app.register_blueprint(products.bp, url_prefix='/products')
# app.register_blueprint(signup.bp, url_prefix='/signup')
# app.register_blueprint(signin.bp, url_prefix='/signin')
# app.register_blueprint(profile.bp, url_prefix='/profile')
# app.register_blueprint(signout.bp, url_prefix='/signout')
# app.register_blueprint(search.bp, url_prefix='/search')
# app.register_blueprint(cart.bp, url_prefix='/cart')
# app.register_blueprint(add_to_cart.bp, url_prefix='/add_to_cart')
# app.register_blueprint(remove_from_cart.bp, url_prefix='/remove_from_cart')
# app.register_blueprint(checkout.bp, url_prefix='/checkout')
# app.register_blueprint(place_order.bp, url_prefix='/place_order')
# app.register_blueprint(order_confirmation.bp, url_prefix='/order_confirmation')
# app.register_blueprint(shipping.bp, url_prefix='/shipping')
# app.register_blueprint(videos.bp, url_prefix='/videos')
# app.register_blueprint(admin_panel.bp, url_prefix='/admin_panel')

app.register_blueprint(landing.bp)
app.register_blueprint(home.bp)
app.register_blueprint(recipe.bp)
app.register_blueprint(products.bp)
app.register_blueprint(signup.bp)
app.register_blueprint(signin.bp)
app.register_blueprint(profile.bp)
app.register_blueprint(signout.bp)
app.register_blueprint(search.bp)
app.register_blueprint(cart.bp)
app.register_blueprint(add_to_cart.bp)
app.register_blueprint(remove_from_cart.bp)
app.register_blueprint(checkout.bp)
app.register_blueprint(place_order.bp)
app.register_blueprint(order_confirmation.bp)
app.register_blueprint(shipping.bp)
app.register_blueprint(videos.bp)
app.register_blueprint(admin_panel.bp)

if __name__ == '__main__':
    app.run(debug=True)