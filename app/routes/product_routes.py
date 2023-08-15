from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField
from wtforms.validators import InputRequired

from app.models import Product
from app.routes.cart_routes import get_cart_count
from app.extensions import db

class ProductForm(FlaskForm):
    name = StringField('Name', validators=[InputRequired()])
    description = TextAreaField('Description', validators=[InputRequired()])
    price = FloatField('Price', validators=[InputRequired()])
    image = StringField('Image', validators=[InputRequired()])
    category = StringField('Category', validators=[InputRequired()])

bp = Blueprint('product_routes', __name__)

@bp.route('/product_list')
def product_list():
    products = Product.query.all()
    return render_template('product_manage.html', products=products)

@bp.route('/products/<int:product_id>')
def show_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return render_template('product_view.html', product=product)
    return {'message': 'Product not found'}, 404


@bp.route('/products/add', methods=['GET', 'POST'])
def add_product():
    form = ProductForm(request.form)
    if request.method == 'POST' and form.validate():
        data = form.data
        product = Product(**data)
        product.save_to_db()
        return redirect(url_for('product_routes.product_list'))
    return render_template('product_add.html', form=form)

@bp.route('/products/edit/<int:product_id>', methods=['GET', 'POST'])
def edit_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {'message': 'Product not found'}, 404
    form = ProductForm(request.form, obj=product)
    if request.method == 'POST' and form.validate():
        form.populate_obj(product)
        product.save_to_db()
        return redirect(url_for('product_routes.product_list'))
    return render_template('product_edit.html', form=form, product=product)

@bp.route('/products/delete/<int:product_id>', methods=['GET', 'POST'])
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {'message': 'Product not found'}, 404
    if request.method == 'POST':
        # Delete the product from the database
        product.delete_from_db()
        return redirect(url_for('product_routes.product_list'))
    return render_template('product_delete.html', product=product)

@bp.route('/shop')
def shop():
    if 'email' in session:
        columns = [getattr(Product, column_name) for column_name in Product.__table__.columns.keys()]
        products = db.session.query(*columns).all()

        cart_count = get_cart_count()
        return render_template('product_shop.html', products=products, cart_count=cart_count)
    else:
        return redirect(url_for('auth_routes.signin'))

@bp.route('/search')
def search():
    if 'email' in session:
        # Get the search query from the request's query parameters
        query = request.args.get('query')
    
        # Search for products matching the query and retrieve them as tuples
        product_columns = [getattr(Product, column_name) for column_name in Product.__table__.columns.keys()]   
        products = db.session.query(*product_columns).filter(
            db.or_(Product.name.ilike(f'%{query}%'), Product.category.ilike(f'%{query}%'), Product.description.ilike(f'%{query}%'))
        ).all()

        # checks items on the cart
        cart_count = get_cart_count()
        
        if session['email'] == 'admin@grocify.com':
            return render_template('product_search_admin.html', products=products, query=query, cart_count=cart_count)
        else:
            # Render the template and pass the product data to it
            return render_template('product_search.html', products=products, query=query, cart_count=cart_count)
    else:
        return redirect(url_for('auth_routes.signin'))