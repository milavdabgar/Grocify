import logging
from logging.handlers import RotatingFileHandler
import os
from flask import Flask

from config import *
from app.extensions import *
from app.routes import auth_routes, home_routes, product_routes, cart_routes, order_routes, recipe_routes
from app.api import ProductResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    api = Api(app)
    db.init_app(app) 
    with app.app_context():
        db.create_all()
    migrate.init_app(app, db, render_as_batch=True)
    
    # Blueprint registrations
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(home_routes.bp)
    app.register_blueprint(product_routes.bp)
    app.register_blueprint(cart_routes.bp)
    app.register_blueprint(order_routes.bp)    
    app.register_blueprint(recipe_routes.bp)    
    
    
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