# from flask import Flask
# from flask_restful import Api
# from flask_sqlalchemy import SQLAlchemy

# import os
# from config import LocalDevelopmentConfig, TestingConfig
# from application.extensions import db
# from application.routes import (
#     auth_routes,
#     home_routes,
#     product_routes,
#     cart_routes,
#     order_routes,
# )
# from application.api import ProductResource


# import logging
# logging.basicConfig(filename='debug.log', level=logging.DEBUG, format=f'%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s')


# app = None
# print("importing the stuff")

# def create_app():
#     # app = Flask(__name__)
#     # app.config.from_object(Config)
#     app = Flask(__name__, template_folder="templates")
#     if os.getenv("ENV", "development") == "production":
#         app.logger.info("Currently no production config is setup.")
#         raise Exception("Currently no production config is setup.")
#     elif os.getenv("ENV", "development") == "testing":
#         app.logger.info("Staring Testing.")
#         print("Staring Testing")
#         app.config.from_object(TestingConfig)
#     else:
#         app.logger.info("Staring Local Development.")
#         print("Staring Local Development")
#         app.config.from_object(LocalDevelopmentConfig)

#     api = Api(app)
#     db.init_app(app)
#     with app.app_context():
#         db.create_all()

#     # Blueprint registrations
#     app.register_blueprint(auth_routes.bp)
#     app.register_blueprint(home_routes.bp)
#     app.register_blueprint(product_routes.bp)
#     app.register_blueprint(cart_routes.bp)
#     app.register_blueprint(order_routes.bp)

#     api.add_resource(
#         ProductResource,
#         "/shop",
#         "/product_list",
#         "/products/<int:product_id>",
#         "/products/add",
#         "/products/edit/<int:product_id>",
#         "/products/delete/<int:product_id>",
#     )
    

#     # Setup Flask-Security
#     # user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
#     # security = Security(app, user_datastore)
    
#     app.logger.info("App setup complete")

#     return app
