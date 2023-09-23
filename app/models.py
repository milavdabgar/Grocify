import base64
from datetime import datetime, timedelta
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
        object_columns = [
            getattr(cls, column_name) for column_name in cls.__table__.columns.keys()
        ]
        objects = (
            db.session.query(*object_columns)
            .filter(
                db.or_(
                    *[
                        getattr(cls, field_name).ilike(f"%{query}%")
                        for field_name in cls.__searchable__
                    ]
                )
            )
            .all()
        )

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


user_products = db.Table(
    "user_products",
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
    db.Column("product_id", db.Integer, db.ForeignKey("product.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    phone = db.Column(db.String(20))
    password_hash = db.Column(db.String(128))
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)
    products = db.relationship("Product", secondary=user_products, backref="users")

    def __repr__(self):
        return "<User {}>".format(self.username)

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
            "username": self.username,
        }
        if include_email:
            data["email"] = self.email
        return data

    def from_dict(self, data, new_user=False):
        for field in ["username", "email", "about_me"]:
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
    __searchable__ = ["name", "description", "category"]
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey("section.id"), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    quantity = db.Column(db.Numeric(10, 2), nullable=True)

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
        return "<Product: {}>".format(self.name)


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class Shipping(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(
        db.Integer, db.ForeignKey("user.id"), nullable=True, default=None
    )
    full_name = db.Column(db.String(255), nullable=True, default=None)
    street_address = db.Column(db.String(255), nullable=True, default=None)
    city = db.Column(db.String(255), nullable=True, default=None)
    state_province = db.Column(db.String(255), nullable=True, default=None)
    postal_code = db.Column(db.String(255), nullable=True, default=None)
    country = db.Column(db.String(255), nullable=True, default=None)


class Cart(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    shipping_id = db.Column(
        db.Integer, db.ForeignKey("shipping.id"), nullable=True, default=None
    )


class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    status = db.Column(db.String(255), nullable=False, default="processing")
    total = db.Column(db.Numeric(10, 2), nullable=False)


class CartProduct(db.Model):
    cart_id = db.Column(db.Integer, db.ForeignKey("cart.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)


class OrderProduct(db.Model):
    order_id = db.Column(db.Integer, db.ForeignKey("order.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("product.id"), primary_key=True)


# from flask_security import UserMixin, RoleMixin
# from flask_sqlalchemy import Model

# class CRUDMixin(Model):
#     @classmethod
#     def create(cls, **kwargs):
#         instance = cls(**kwargs)
#         db.session.add(instance)
#         db.session.commit()
#         return instance

#     @classmethod
#     def read(cls, id):
#         return cls.query.get(id)

#     def update(self, **kwargs):
#         for key, value in kwargs.items():
#             setattr(self, key, value)
#         db.session.commit()

#     def delete(self):
#         db.session.delete(self)
#         db.session.commit()


# roles_users = db.Table(
#     "roles_users",
#     db.Column("user_id", db.Integer(), db.ForeignKey("User.id")),
#     db.Column("role_id", db.Integer(), db.ForeignKey("Role.id")),
# )

# class User(db.Model, UserMixin, CRUDMixin):
#     __tablename__ = "User"
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     name = db.Column(db.String(255), nullable=False)
#     email = db.Column(db.String(255), nullable=False, unique=True)
#     password = db.Column(db.String(255), nullable=False)
#     phone = db.Column(db.String(20), nullable=False)
# fs_uniquifier = db.Column(db.String(64), unique=True)
# role_id = db.Column(db.Integer, db.ForeignKey("Role.id"), nullable=False)
# roles = db.relationship(
#     "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
# )


# class Role(db.Model, RoleMixin, CRUDMixin):
#     __tablename__ = "Role"
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(80), unique=True)
#     description = db.Column(db.String(255))

# @login.user_loader
# def load_user(id):
#     return User.query.get(int(id))
