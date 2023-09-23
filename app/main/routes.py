from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g, current_app
from flask_login import current_user, login_required
from app import db
from app.main.forms import EditProfileForm, EmptyForm, SearchForm
from app.models import User, Product
from app.main import bp
from app.api.products_api import ProductForm

@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
        g.search_form = SearchForm()


@bp.route('/', methods=['GET', 'POST'])
@bp.route('/index', methods=['GET', 'POST'])
@login_required
# def index():
#     products = Product.query.all()
#     return render_template('product/product_shop.html', products=products)
def index():
    form = ProductForm()
    if form.validate_on_submit():
        product = Product(body=form.product.data, author=current_user)
        db.session.add(product)
        db.session.commit()
        flash('Your product is now live!')
        return redirect(url_for('main.index'))
    page = request.args.get('page', 1, type=int)
    products = current_user.followed_products().paginate( page=page, per_page=current_app.config['PRODUCTS_PER_PAGE'], error_out=False)
    next_url = url_for('main.index', page=products.next_num) if products.has_next else None
    prev_url = url_for('main.index', page=products.prev_num) if products.has_prev else None
    return render_template('index.html', title='Home', form=form, products=products.items, next_url=next_url, prev_url=prev_url)


@bp.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    products = Product.query.order_by(Product.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['PRODUCTS_PER_PAGE'],
        error_out=False)
    next_url = url_for('main.explore', page=products.next_num) if products.has_next else None
    prev_url = url_for('main.explore', page=products.prev_num) if products.has_prev else None
    return render_template('index.html', title='Explore', products=products.items, next_url=next_url, prev_url=prev_url)


@bp.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    products = user.products.order_by(Product.timestamp.desc()).paginate(
        page=page, per_page=current_app.config['PRODUCTS_PER_PAGE'],
        error_out=False)
    next_url = url_for('main.user', username=user.username, page=products.next_num) if products.has_next else None
    prev_url = url_for('main.user', username=user.username, page=products.prev_num) if products.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, products=products.items, next_url=next_url, prev_url=prev_url, form=form)


@bp.route('/user/<username>/popup')
@login_required
def user_popup(username):
    user = User.query.filter_by(username=username).first_or_404()
    form = EmptyForm()
    return render_template('user_popup.html', user=user, form=form)


@bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('main.edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile', form=form)


@bp.route('/search')
@login_required
def search():
    if not g.search_form.validate():
        return redirect(url_for('main.explore'))
    page = request.args.get('page', 1, type=int)
    products, total = Product.search(g.search_form.q.data, page, current_app.config['PRODUCTS_PER_PAGE'])
    next_url = url_for('main.search', q=g.search_form.q.data, page=page + 1) if total > page * current_app.config['PRODUCTS_PER_PAGE'] else None
    prev_url = url_for('main.search', q=g.search_form.q.data, page=page - 1) if page > 1 else None
    return render_template('search.html', title='Search', products=products, next_url=next_url, prev_url=prev_url)