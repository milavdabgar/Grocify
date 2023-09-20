import os
import logging

from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_mail import Mail
from flask_restful import Api
from flask_login import LoginManager, login_user, current_user
from werkzeug.security import check_password_hash
from flask_security import (
    Security,
    SQLAlchemySessionUserDatastore,
    SQLAlchemyUserDatastore,
)

from application.models import User, Role
from application.forms import LoginForm, RegisterForm
from application.config import LocalDevelopmentConfig, TestingConfig
from application.api import ProductResource
from application.extensions import db
from application.routes import (
    auth_routes,
    home_routes,
    product_routes,
    cart_routes,
    order_routes,
)


logging.basicConfig(
    filename="logs/debug.log",
    level=logging.DEBUG,
    format=f"%(asctime)s %(levelname)s %(name)s %(threadName)s : %(message)s",
)


app = None
print("importing the stuff")

# def create_app():
# app = Flask(__name__)
# app.config.from_object(Config)
app = Flask(
    __name__,
    template_folder="application/templates",
    static_folder="application/static",
)

# Configurations
if os.getenv("ENV", "development") == "production":
    app.logger.info("Currently no production config is setup.")
    raise Exception("Currently no production config is setup.")
elif os.getenv("ENV", "development") == "testing":
    app.logger.info("Staring Testing.")
    print("Staring Testing")
    app.config.from_object(TestingConfig)
else:
    app.logger.info("Staring Local Development.")
    print("Staring Local Development")
    app.config.from_object(LocalDevelopmentConfig)


# Initialize extensions

api = Api(app)
mail = Mail(app)
# db = SQLAlchemy(app)
db.init_app(app)
with app.app_context():
    db.create_all()
migrate = Migrate(app, db)
app.app_context().push()
login_manager = LoginManager(app)
login_manager.login_view = "login"

# Setup Flask-Security
user_datastore = SQLAlchemySessionUserDatastore(db.session, User, Role)
security = Security(app, user_datastore)


# Blueprint registrations
app.register_blueprint(auth_routes.bp)
app.register_blueprint(home_routes.bp)
app.register_blueprint(product_routes.bp)
app.register_blueprint(cart_routes.bp)
app.register_blueprint(order_routes.bp)


api.add_resource(
    ProductResource,
    "/shop",
    "/product_list",
    "/products/<int:product_id>",
    "/products/add",
    "/products/edit/<int:product_id>",
    "/products/delete/<int:product_id>",
)


app.logger.info("App setup complete")

# # return app

# Import all the controllers so they are loaded
print("importing the stuff")
# from application.routes import *


@app.errorhandler(404)
def page_not_found(e):
    # note that we set the 404 status explicitly
    return render_template("404.html"), 404


@app.errorhandler(403)
def not_authorized(e):
    # note that we set the 403 status explicitly
    return render_template("403.html"), 403


# User model
class Userr(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    # Replace this with your own logic to load a user object based on the user_id
    return Userr.query.get(int(user_id))


# Routes
@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))

    form = LoginForm()  # Create an instance of your LoginForm

    if request.method == "POST" and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = Userr.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("home"))
        else:
            return "Invalid email or password"

    return render_template(
        "login.html", form=form
    )  # Pass the form object to the template context


@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        # Perform registration logic
        user = Userr(username=form.username.data, email=form.email.data)
        db.session.add(user)
        db.session.commit()
        return "Registered successfully"
    return render_template("register.html", form=form)


if __name__ == "__main__":
    app.run(debug=True)
