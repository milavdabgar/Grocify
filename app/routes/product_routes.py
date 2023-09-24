from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, FloatField, IntegerField, SubmitField
from wtforms.validators import InputRequired

from app.models import Product
from app.routes.cart_routes import get_cart_count
from app import db
from flask_login import current_user, login_required


class ProductForm(FlaskForm):
    name = StringField("Name", validators=[InputRequired()])
    description = TextAreaField("Description", validators=[InputRequired()])
    price = FloatField("Price", validators=[InputRequired()])
    image = StringField("Image", validators=[InputRequired()])
    category = StringField("Category", validators=[InputRequired()])
    quantity = IntegerField("Quantity", validators=[InputRequired()])
    submit = SubmitField("Submit")


bp = Blueprint("product_routes", __name__)


@bp.route("/product_list")
@login_required
def product_list():
    products = Product.query.all()
    return render_template("product/product_manage.html", products=products)


@bp.route("/products/<int:product_id>")
@login_required
def show_product(product_id):
    product = Product.query.get(product_id)
    if product:
        return render_template("product/product_view.html", product=product)
    return {"message": "Product not found"}, 404


@bp.route("/products/add", methods=["GET", "POST"])
@login_required
# @roles_required('admin')
def add_product():
    form = ProductForm()
    if request.method == "POST" and form.validate_on_submit():
        data = form.data
        product = Product(
            name=data["name"],
            description=data["description"],
            price=data["price"],
            image=data["image"],
            category=data["category"],
            quantity=data["quantity"],
        )  # adjust the fields according to your Product class
        product.save_to_db()
        return redirect(url_for("product_routes.product_list"))
    return render_template("product/product_add.html", form=form)


@bp.route("/products/edit/<int:product_id>", methods=["GET", "POST"])
@login_required
# @roles_required('admin')
def edit_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {"message": "Product not found"}, 404
    form = ProductForm(request.form, obj=product)
    if request.method == "POST" and form.validate():
        form.populate_obj(product)
        product.save_to_db()
        return redirect(url_for("product_routes.product_list"))
    return render_template("product/product_edit.html", form=form, product=product)


@bp.route("/products/delete/<int:product_id>", methods=["GET", "POST"])
@login_required
# @roles_required('admin')
def delete_product(product_id):
    product = Product.query.get(product_id)
    if not product:
        return {"message": "Product not found"}, 404
    if request.method == "POST":
        # Delete the product from the database
        product.delete_from_db()
        return redirect(url_for("product_routes.product_list"))
    return render_template("product/product_delete.html", product=product)


@bp.route("/shop")
@login_required
def shop():
    columns = [
        getattr(Product, column_name)
        for column_name in Product.__table__.columns.keys()
    ]
    products = db.session.query(*columns).all()

    cart_count = get_cart_count()
    return render_template(
        "product/product_shop.html", products=products, cart_count=cart_count
    )
