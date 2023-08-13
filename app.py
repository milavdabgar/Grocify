from flask import Flask
from routes import landing, home, recipe, products, signup, signin, profile, signout, search, cart, add_to_cart, remove_from_cart, checkout, place_order, order_confirmation, shipping, videos, admin_panel
import os
from config import *
from extensions import db
import urllib.parse

password = 'Seagate@123'
encoded_password = urllib.parse.quote_plus(password)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fresh_basket_sample.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{encoded_password}@localhost/fresh_basket_sample'
app.secret_key = os.environ.get('APP_SECRET_KEY')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app) 

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