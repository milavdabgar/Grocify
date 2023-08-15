from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocify_sample.sqlite'
db = SQLAlchemy(app)

class Cart(db.Model):
    __tablename__ = 'Cart'
    Id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.Id'), nullable=False)
    ShippingId = db.Column(db.Integer, db.ForeignKey('Shipping.Id'), nullable=True)

class CartProduct(db.Model):
    __tablename__ = 'CartProduct'
    CartId = db.Column(db.Integer, db.ForeignKey('Cart.Id'), primary_key=True)
    ProductId = db.Column(db.Integer, db.ForeignKey('Product.Id'), primary_key=True)

class Order(db.Model):
    __tablename__ = 'Order'
    Id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.Id'), nullable=False)
    Status = db.Column(db.String(255), nullable=False, default='processing')
    Total = db.Column(db.Numeric(10, 2), nullable=False)

class OrderProduct(db.Model):
    __tablename__ = 'OrderProduct'
    OrderId = db.Column(db.Integer, db.ForeignKey('Order.Id'), primary_key=True)
    ProductId = db.Column(db.Integer, db.ForeignKey('Product.Id'), primary_key=True)

class Product(db.Model):
    __tablename__ = 'Product'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Description = db.Column(db.String(255), nullable=False)
    Price = db.Column(db.Numeric(10, 2), nullable=False)
    Image = db.Column(db.String(255), nullable=False)
    Category = db.Column(db.String(255), nullable=False)
    product_Id = db.Column(db.String(255), nullable=False)

class Shipping(db.Model):
    __tablename__ = 'Shipping'
    Id = db.Column(db.Integer, primary_key=True)
    UserId = db.Column(db.Integer, db.ForeignKey('User.Id'), nullable=True)
    Full_Name = db.Column(db.String(255), nullable=True)
    Street_Address = db.Column(db.String(255), nullable=True)
    City = db.Column(db.String(255), nullable=True)
    State_Province = db.Column(db.String(255), nullable=True)
    Postal_Code = db.Column(db.String(255), nullable=True)
    Country = db.Column(db.String(255), nullable=True)

class User(db.Model):
    __tablename__ = 'User'
    Id = db.Column(db.Integer, primary_key=True)
    Name = db.Column(db.String(255), nullable=False)
    Email = db.Column(db.String(255), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    Phone = db.Column(db.String(20), nullable=False)


with app.app_context():
    db.create_all()
    
    # Insert the values into the "Cart" table
    cart1 = Cart(Id=1, UserId=17, ShippingId=0)
    cart2 = Cart(Id=2, UserId=18, ShippingId=0)
    cart3 = Cart(Id=3, UserId=16, ShippingId=0)
    cart4 = Cart(Id=5, UserId=20, ShippingId=None)
    cart5 = Cart(Id=6, UserId=21, ShippingId=None)
    cart6 = Cart(Id=7, UserId=22, ShippingId=None)
    cart7 = Cart(Id=8, UserId=23, ShippingId=None)
    cart8 = Cart(Id=9, UserId=24, ShippingId=None)
    
    db.session.add_all([cart1, cart2, cart3, cart4, cart5, cart6, cart7, cart8])
    db.session.commit()  # Commit the changes to the database