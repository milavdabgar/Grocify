from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import csv
import urllib.parse

password = 'Seagate@123'
encoded_password = urllib.parse.quote_plus(password)

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocify_sample.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocify_sample.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:"Seagate@123"@localhost/grocify_sample'
app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{encoded_password}@localhost/grocify_sample'

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
    product_id = db.Column(db.String(255), nullable=False)

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
    
# Define a dictionary to map each table to its corresponding CSV file
table_csv_mapping = {
    Product: 'imports/Product.csv',
    User: 'imports/User.csv',
    Shipping: 'imports/Shipping.csv',
    Cart: 'imports/Cart.csv',
    CartProduct: 'imports/CartProduct.csv',
    Order: 'imports/Order.csv',
    OrderProduct: 'imports/OrderProduct.csv',                    
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
