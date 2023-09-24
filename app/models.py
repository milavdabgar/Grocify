import base64
from datetime import datetime, timedelta, timezone
from hashlib import md5
import json
import os
from time import time
from flask import current_app, url_for
from flask_login import UserMixin, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login
from app.search import add_to_index, remove_from_index, query_index


class SearchableMixin(object):
    @classmethod
    def search_db(cls, query, page, per_page):
        objects = cls.query.filter(
            db.or_(
                *[
                    getattr(cls, field_name).ilike(f"%{query}%")
                    for field_name in cls.__searchable__
                ]
            )
        ).all()

        total = len(objects)

        return objects, total

    @classmethod
    def search(cls, expression, page, per_page):
        ids, total = query_index(cls.__tablename__, expression, page, per_page)
        if total == 0:
            return cls.query.filter_by(id=0), 0
        when = {}
        for i in range(len(ids)):
            when[ids[i]] = i
        return (
            cls.query.filter(cls.id.in_(ids)).order_by(db.case(when, value=cls.id)),
            total,
        )
        # when = []
        # for i in range(len(ids)):
        #     when.append((ids[i], i))
        # return cls.query.filter(cls.id.in_(ids)).order_by(
        #     db.case(when, value=cls.id)), total

    @classmethod
    def before_commit(cls, session):
        session._changes = {
            "add": list(session.new),
            "update": list(session.dirty),
            "delete": list(session.deleted),
        }

    @classmethod
    def after_commit(cls, session):
        for obj in session._changes["add"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["update"]:
            if isinstance(obj, SearchableMixin):
                add_to_index(obj.__tablename__, obj)
        for obj in session._changes["delete"]:
            if isinstance(obj, SearchableMixin):
                remove_from_index(obj.__tablename__, obj)
        session._changes = None

    @classmethod
    def reindex(cls):
        for obj in cls.query:
            add_to_index(cls.__tablename__, obj)


db.event.listen(db.session, "before_commit", SearchableMixin.before_commit)
db.event.listen(db.session, "after_commit", SearchableMixin.after_commit)


class PaginatedAPIMixin(object):
    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page=page, per_page=per_page, error_out=False)
        data = {
            "items": [item.to_dict() for item in resources.items],
            "_meta": {
                "page": page,
                "per_page": per_page,
                "total_pages": resources.pages,
                "total_items": resources.total,
            },
            "_links": {
                "self": url_for(endpoint, page=page, per_page=per_page, **kwargs),
                "next": url_for(endpoint, page=page + 1, per_page=per_page, **kwargs)
                if resources.has_next
                else None,
                "prev": url_for(endpoint, page=page - 1, per_page=per_page, **kwargs)
                if resources.has_prev
                else None,
            },
        }
        return data


UserProducts = db.Table(
    "UserProducts",
    db.Column("user_id", db.Integer, db.ForeignKey("User.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("Product.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    __tablename__ = "User"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    user_name = db.Column(db.String(50), index=True, unique=True)
    email = db.Column(db.String(100), index=True, unique=True, nullable=False)
    contact = db.Column(db.String(15), unique=True)
    password_hash = db.Column(db.String(500))
    date_joined = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    products = db.relationship("Product", secondary=UserProducts, backref="users")

    def __repr__(self):
        """
        Special method represents an object of User class when printed
        """
        return f"<User : {self.id} -> {self.full_name} ({self.user_name})>"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {"reset_password": self.id, "exp": time() + expires_in},
            current_app.config["SECRET_KEY"],
            algorithm="HS256",
        )

    def listed_products(self):
        my_products = Product.query.filter_by(user_id=self.id)
        return my_products

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(
                token, current_app.config["SECRET_KEY"], algorithms=["HS256"]
            )["reset_password"]
        except:
            return
        return User.query.get(id)

    def to_dict(self, include_email=False):
        data = {
            "id": self.id,
            "user_name": self.user_name,
        }
        if include_email:
            data["email"] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ["user_name", "email", "full_name"]:
            if field in data:
                setattr(self, field, data[field])
        if new_user and "password" in data:
            self.set_password(data["password"])

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(seconds=expires_in)
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Product(db.Model, SearchableMixin, PaginatedAPIMixin):
    __tablename__ = "Product"
    __searchable__ = ["name", "description", "category"]
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500))
    # price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.Integer, db.ForeignKey("Category.id"), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    unit = db.Column(db.Integer, db.ForeignKey("MeasurementUnit.id"), nullable=False)
    price_per_quantity = db.Column(db.Integer, nullable=False)
    seller = db.Column(db.Integer, db.ForeignKey("Seller.id"), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    expiration_date = db.Column(db.DateTime, nullable=False)
    rating = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"))

    # def json(self):
    #     return {
    #         "id": self.id,
    #         "name": self.name,
    #         "description": self.description,
    #         "price": str(self.price),
    #         "image": self.image,
    #         "category": self.category,
    #     }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def __repr__(self):
        """
        Special method represents an object of Product class when printed
        """
        return f"<Product : {self.id} -> {self.name}>"


class Shipping(db.Model):
    __tablename__ = "Shipping"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("User.id"), nullable=True, default=None
    )
    full_name = db.Column(db.String(255), nullable=True, default=None)
    street_address = db.Column(db.String(255), nullable=True, default=None)
    city = db.Column(db.String(255), nullable=True, default=None)
    state_province = db.Column(db.String(255), nullable=True, default=None)
    postal_code = db.Column(db.String(255), nullable=True, default=None)
    country = db.Column(db.String(255), nullable=True, default=None)


class Cart(db.Model):
    __tablename__ = "Cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    shipping_id = db.Column(
        db.Integer, db.ForeignKey("Shipping.id"), nullable=True, default=None
    )


class Order(db.Model):
    __tablename__ = "Order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    status = db.Column(db.String(255), nullable=False, default="processing")
    total = db.Column(db.Numeric(10, 2), nullable=False)


class CartProduct(db.Model):
    __tablename__ = "CartProduct"
    cart_id = db.Column(db.Integer, db.ForeignKey("Cart.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"), primary_key=True)


class OrderProduct(db.Model):
    __tablename__ = "OrderProduct"
    order_id = db.Column(db.Integer, db.ForeignKey("Order.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"), primary_key=True)


class Admin(db.Model):
    __tablename__ = "Admin"

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(100))
    user_name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(100), unique=True)
    contact = db.Column(db.String(15), unique=True)
    password_hash = db.Column(db.String(500))

    def __repr__(self):
        return f"<Admin : {self.id} -> {self.user_name}>"


class City(db.Model):
    __tablename__ = "City"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<City : {self.id} -> {self.name}>"


class State(db.Model):
    __tablename__ = "State"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<State : {self.id} -> {self.name}>"


class Country(db.Model):
    __tablename__ = "Country"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Country : {self.id} -> {self.name}>"


class Location(db.Model):
    __tablename__ = "Location"

    id = db.Column(db.Integer, primary_key=True)
    city_id = db.Column(db.Integer, db.ForeignKey("City.id"), nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey("State.id"), nullable=False)
    country_id = db.Column(db.Integer, db.ForeignKey("Country.id"), nullable=False)


class PrimaryAddress(db.Model):
    __tablename__ = "PrimaryAddress"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    address_id = db.Column(db.Integer, db.ForeignKey("Address.id"), nullable=False)

    def __repr__(self):
        return f"<PrimaryAddress : {self.user_id} -> {self.address_id}>"


class Address(db.Model):
    __tablename__ = "Address"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50))
    house_number = db.Column(db.String(50))
    line_1 = db.Column(db.String(200), nullable=False)
    line_2 = db.Column(db.String(200))
    pincode = db.Column(db.String(6), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey("Location.id"), nullable=False)

    def __repr__(self):
        return f"<Address : {self.id} -> {self.user_id}>"


class Category(db.Model):
    __tablename__ = "Category"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500))

    def __repr__(self):
        return f"<Category : {self.id} -> {self.name}>"


class MeasurementUnit(db.Model):
    __tablename__ = "MeasurementUnit"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    shorthand = db.Column(db.String(10), unique=True, nullable=True)

    def __repr__(self):
        return f"<MeasurementUnit : {self.id} -> {self.name} ({self.shorthand})>"


class Rating(db.Model):
    __tablename__ = "Rating"

    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    stars = db.Column(db.Integer, nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.now(timezone.utc))
    description = db.Column(db.String(500))

    def __repr__(self):
        return f"<Rating : {self.product_id} -> {self.stars}>"


class Seller(db.Model):
    __tablename__ = "Seller"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    seller_contact = db.Column(db.String(20), nullable=False)
    seller_email = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return f"<Seller : {self.id} -> {self.name}>"
