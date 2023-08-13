from flask import Blueprint, render_template
from app.controllers import get_cart_count

from app.models import Product
from app.extensions import db

bp = Blueprint('products', __name__)

@bp.route('/products')
def products():
    columns = [getattr(Product, column_name) for column_name in Product.__table__.columns.keys()]
    products = db.session.query(*columns).all()

    cart_count = get_cart_count()
    return render_template('shop.html', products=products, cart_count=cart_count)