from flask import Blueprint, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField
from wtforms.validators import InputRequired

from app.models import Product
from app.controllers import get_cart_count
from app.extensions import db

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    price = FloatField('Price', validators=[InputRequired()])
    image = StringField('Image', validators=[InputRequired()])
    category = StringField('Category', validators=[InputRequired()])

bp = Blueprint('product_forms', __name__)

@bp.route('/product_list')
def product_list():
    products = Product.query.all()
    return render_template('product_list.html', products=products)

@bp.route('/products/<int:product_id>')
def show_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return render_template('product.html', product=product)
    return {'message': 'Product not found'}, 404


@bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm(request.form)
    if request.method == 'POST' and form.validate():
        data = form.data
        product = Product(**data)
        product.save_to_db()
        return redirect(url_for('product_forms.product_list'))
    return render_template('add_product.html', form=form)

@bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {'message': 'Product not found'}, 404
    form = ProductForm(request.form, obj=product)
    if request.method == 'POST' and form.validate():
        form.populate_obj(product)
        product.save_to_db()
        return redirect(url_for('product_forms.product_list'))
    return render_template('edit_product.html', form=form, product=product)

@bp.route('/products/delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {'message': 'Product not found'}, 404
    if request.method == 'POST':
        # Delete the product from the database
        product.delete_from_db()
        return redirect(url_for('product_forms.product_list'))
    return render_template('delete_product.html', product=product)



@bp.route('/shop')
def shop():
    columns = [getattr(Product, column_name) for column_name in Product.__table__.columns.keys()]
    products = db.session.query(*columns).all()

    cart_count = get_cart_count()
    return render_template('shop.html', products=products, cart_count=cart_count)