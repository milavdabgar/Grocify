from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, EmptyForm, SearchForm
from app.models import User, Product
from app.main import bp
from app.api.products_api import ProductForm

# from app.routes.cart_routes import get_cart_count


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()


@bp.route("/", methods=["GET", "POST"])
@bp.route("/index", methods=["GET", "POST"])
@login_required
def index():
    return render_template("main/index.html")
    # form = ProductForm()
    # if request.method == "POST" and form.validate_on_submit():
    #     data = form.data
    #     product = Product(
    #         name=data["name"],
    #         description=data["description"],
    #         price=data["price"],
    #         image=data["image"],
    #         category=data["category"],
    #         quantity=data["quantity"],
    #         user_id=current_user.id,
    #     )  # adjust the fields according to your Product class
    #     product.save_to_db()
    #     flash("Your product is now live!")
    #     return redirect(url_for("main.index"))
    # page = request.args.get("page", 1, type=int)
    # products = current_user.listed_products().paginate(
    #     page=page, per_page=current_app.config["PRODUCTS_PER_PAGE"], error_out=False
    # )
    # next_url = (
    #     url_for("main.index", page=products.next_num) if products.has_next else None
    # )
    # prev_url = (
    #     url_for("main.index", page=products.prev_num) if products.has_prev else None
    # )
    # return render_template(
    #     "index.html",
    #     title="Home",
    #     form=form,
    #     products=products.items,
    #     next_url=next_url,
    #     prev_url=prev_url,
    # )


@bp.route("/explore")
@login_required
def explore():
    page = request.args.get("page", 1, type=int)
    products = Product.query.order_by(Product.name.desc()).paginate(
        page=page, per_page=current_app.config["PRODUCTS_PER_PAGE"], error_out=False
    )
    next_url = (
        url_for("main.explore", page=products.next_num) if products.has_next else None
    )
    prev_url = (
        url_for("main.explore", page=products.prev_num) if products.has_prev else None
    )
    return render_template(
        "index.html",
        title="Explore",
        products=products.items,
        next_url=next_url,
        prev_url=prev_url,
    )


@bp.route("/user/<user_name>")
@login_required
def user(user_name):
    user = User.query.filter_by(user_name=user_name).first_or_404()
    page = request.args.get("page", 1, type=int)

    products = current_user.listed_products().paginate(
        page=page, per_page=current_app.config["PRODUCTS_PER_PAGE"], error_out=False
    )

    next_url = (
        url_for("main.user", user_name=user.user_name, page=products.next_num)
        if products.has_next
        else None
    )
    prev_url = (
        url_for("main.user", user_name=user.user_name, page=products.prev_num)
        if products.has_prev
        else None
    )
    form = EmptyForm()
    return render_template(
        "user.html",
        user=user,
        products=products.items,
        next_url=next_url,
        prev_url=prev_url,
        form=form,
    )


@bp.route("/user/<user_name>/popup")
@login_required
def user_popup(user_name):
    user = User.query.filter_by(user_name=user_name).first_or_404()
    form = EmptyForm()
    return render_template("user_popup.html", user=user, form=form)


@bp.route("/edit_profile", methods=["GET", "POST"])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.user_name)
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.user_name = form.user_name.data
        current_user.email = form.email.data
        current_user.contact = form.contact.data
        db.session.commit()
        flash("Your changes have been saved.")
        return redirect(url_for("main.edit_profile"))
    elif request.method == "GET":
        form.name.data = current_user.name
        form.user_name.data = current_user.user_name
        form.email.data = current_user.email
        form.contact.data = current_user.contact
    return render_template("edit_profile.html", title="Edit Profile", form=form)


@bp.route("/search")
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for("main.explore"))
    page = request.args.get("page", 1, type=int)
    # cart_count = get_cart_count()
    if current_app.elasticsearch:
        products, total = Product.search(
            g.search_form.q.data, page, current_app.config["PRODUCTS_PER_PAGE"]
        )
    else:
        products, total = Product.search_db(
            g.search_form.q.data, page, current_app.config["PRODUCTS_PER_PAGE"]
        )
    next_url = (
        url_for("main.search", q=g.search_form.q.data, page=page + 1)
        if total > page * current_app.config["PRODUCTS_PER_PAGE"]
        else None
    )
    prev_url = (
        url_for("main.search", q=g.search_form.q.data, page=page - 1)
        if page > 1
        else None
    )
    return render_template(
        "search.html",
        title="Search",
        products=products,
        next_url=next_url,
        prev_url=prev_url,
    )
