from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocify_sample.sqlite'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocify_sample.sqlite'
db = SQLAlchemy(app)

class Cart(db.Model):
    __tablename__ = 'Cart'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    shipping_id = db.Column(db.Integer, db.ForeignKey('Shipping.id'), nullable=True)

class CartProduct(db.Model):
    __tablename__ = 'CartProduct'
    cart_id = db.Column(db.Integer, db.ForeignKey('Cart.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'), primary_key=True)

class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    status = db.Column(db.String(255), nullable=False, default='processing')
    total = db.Column(db.Numeric(10, 2), nullable=False)

class OrderProduct(db.Model):
    __tablename__ = 'OrderProduct'
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'), primary_key=True)

class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    product_id = db.Column(db.String(255), nullable=False)

class Shipping(db.Model):
    __tablename__ = 'Shipping'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=True)
    full_name = db.Column(db.String(255), nullable=True)
    street_address = db.Column(db.String(255), nullable=True)
    city = db.Column(db.String(255), nullable=True)
    state_province = db.Column(db.String(255), nullable=True)
    postal_code = db.Column(db.String(255), nullable=True)
    country = db.Column(db.String(255), nullable=True)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(20), nullable=False)
    
# Define a dictionary to map each table to its corresponding CSV file
table_csv_mapping = {
    Cart: 'imports/Cart.csv',
    CartProduct: 'imports/CartProduct.csv',
    Order: 'imports/Order.csv',
    OrderProduct: 'imports/OrderProduct.csv',
    Product: 'imports/Product.csv',
    Shipping: 'imports/Shipping.csv',
    User: 'imports/User.csv',                  
}

# Iterate over each table and CSV file
# Iterate over each table and CSV file
with app.app_context():
    db.create_all()
    for table, csv_file in table_csv_mapping.items():
        # Read the CSV file
        with open(csv_file, 'r') as file:
            reader = csv.DictReader(file)
            data = [dict(row) for row in reader]

        # Insert the data into the table
        for row in data:
            obj = table(**row)
            db.session.add(obj)
        db.session.commit()
