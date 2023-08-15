from flask import Flask
from flask_restful import Api
from flask_sqlalchemy import SQLAlchemy


from config import Config
from app.extensions import db
from app.routes import auth_routes, home_routes, product_routes, cart_routes, order_routes
from app.api import ProductResource

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    api = Api(app)
    db.init_app(app) 
    with app.app_context():
        db.create_all()
    
    # Blueprint registrations
    app.register_blueprint(auth_routes.bp)
    app.register_blueprint(home_routes.bp)
    app.register_blueprint(product_routes.bp)
    app.register_blueprint(cart_routes.bp)
    app.register_blueprint(order_routes.bp)    
    
    api.add_resource(ProductResource, '/shop', '/product_list', '/products/<int:product_id>', '/products/add', '/products/edit/<int:product_id>', '/products/delete/<int:product_id>')

    return app