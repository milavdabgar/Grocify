from flask import Blueprint

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
def home():
    return "Hello, this is the home page!"
