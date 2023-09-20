from application.extensions import db
from flask_security import UserMixin, RoleMixin
from flask_login import login_manager

from flask_sqlalchemy import SQLAlchemy, Model

# db = SQLAlchemy()


class CRUDMixin(Model):
    @classmethod
    def create(cls, **kwargs):
        instance = cls(**kwargs)
        db.session.add(instance)
        db.session.commit()
        return instance

    @classmethod
    def read(cls, id):
        return cls.query.get(id)

    def update(self, **kwargs):
        for key, value in kwargs.items():
            setattr(self, key, value)
        db.session.commit()

    def delete(self):
        db.session.delete(self)
        db.session.commit()


class User(db.Model, UserMixin, CRUDMixin):
    __tablename__ = "User"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    fs_uniquifier = db.Column(db.String(64), unique=True)
    role_id = db.Column(db.Integer, db.ForeignKey("Role.id"), nullable=False)
    # roles = db.relationship(
    #     "Role", secondary=roles_users, backref=db.backref("users", lazy="dynamic")
    # )


class Role(db.Model, RoleMixin, CRUDMixin):
    __tablename__ = "Role"
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))


class Product(db.Model, CRUDMixin):
    __tablename__ = "Product"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    section_id = db.Column(db.Integer, db.ForeignKey("Section.id"), nullable=False)
    quantity = db.Column(db.Numeric(10, 2), nullable=True)

    def json(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "price": str(self.price),
            "image": self.image,
            "category": self.category,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()


class Section(db.Model):
    __tablename__ = "Section"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)


class Shipping(db.Model, CRUDMixin):
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


class Cart(db.Model, CRUDMixin):
    __tablename__ = "Cart"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    shipping_id = db.Column(
        db.Integer, db.ForeignKey("Shipping.id"), nullable=True, default=None
    )


class Order(db.Model, CRUDMixin):
    __tablename__ = "Order"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey("User.id"), nullable=False)
    status = db.Column(db.String(255), nullable=False, default="processing")
    total = db.Column(db.Numeric(10, 2), nullable=False)


class CartProduct(db.Model, CRUDMixin):
    __tablename__ = "CartProduct"
    cart_id = db.Column(db.Integer, db.ForeignKey("Cart.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"), primary_key=True)


class OrderProduct(db.Model, CRUDMixin):
    __tablename__ = "OrderProduct"
    order_id = db.Column(db.Integer, db.ForeignKey("Order.id"), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey("Product.id"), primary_key=True)


roles_users = db.Table(
    "roles_users",
    db.Column("user_id", db.Integer(), db.ForeignKey("User.id")),
    db.Column("role_id", db.Integer(), db.ForeignKey("Role.id")),
)
