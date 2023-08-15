import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask

from config import *
from app.extensions import *
from app.views import landing, home, product_forms, recipe, signup, signin, profile, signout, search, cart, add_to_cart, remove_from_cart, checkout, place_order, order_confirmation, shipping, videos, admin_panel
from app.api.products import ProductResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    api = Api(app)
    db.init_app(app) 
    with app.app_context():
        db.create_all()
    migrate.init_app(app, db, render_as_batch=True)
    
    # Blueprint registrations
    app.register_blueprint(landing.bp)
    app.register_blueprint(home.bp)
    app.register_blueprint(recipe.bp)
    app.register_blueprint(signup.bp)
    app.register_blueprint(signin.bp)
    app.register_blueprint(profile.bp)
    app.register_blueprint(signout.bp)
    app.register_blueprint(search.bp)
    app.register_blueprint(cart.bp)
    app.register_blueprint(add_to_cart.add_to_cart_bp)
    app.register_blueprint(remove_from_cart.bp)
    app.register_blueprint(checkout.bp)
    app.register_blueprint(place_order.bp)
    app.register_blueprint(order_confirmation.bp)
    app.register_blueprint(shipping.bp)
    app.register_blueprint(videos.bp)
    app.register_blueprint(admin_panel.bp)
    
    app.register_blueprint(product_forms.bp)
    
    api.add_resource(ProductResource, '/shop', '/product_list', '/products/<int:product_id>', '/products/add', '/products/edit/<int:product_id>', '/products/delete/<int:product_id>')
    
    if not app.debug and not app.testing:
        if app.config['LOG_TO_STDOUT']:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists('logs'):
                os.mkdir('logs')
            file_handler = RotatingFileHandler('logs/grocify.log', maxBytes=10240, backupCount=10)
            file_handler.setFormatter(logging.Formatter(
                '%(asctime)s %(levelname)s: %(message)s '
                '[in %(pathname)s:%(lineno)d]'))
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

    app.logger.setLevel(logging.INFO)
    app.logger.info('Grocify startup')

    return app

# from app import models