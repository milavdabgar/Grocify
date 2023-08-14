from flask import Flask, Blueprint, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField
from wtforms.validators import DataRequired
from app.models import Product

class AddProductForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired()])
    image = StringField('Image URL', validators=[DataRequired()])
    category = StringField('Category', validators=[DataRequired()])

add_product_bp = Blueprint('add_product', __name__)

@add_product_bp.route('/add_product', methods=['GET', 'POST'])
def add_product():
    form = AddProductForm()

    if form.validate_on_submit():
        # Process form submission
        name = form.name.data
        description = form.description.data
        price = form.price.data
        image = form.image.data
        category = form.category.data

        # Create new product instance
        data = {
            'name': name,
            'description': description,
            'price': price,
            'image': image,
            'category': category
        }
        product = Product(**data)
        product.save_to_db()

        return f"Product '{product.name}' added successfully!"

    # Render the form template for GET request
    return render_template('add_product.html', form=form)
