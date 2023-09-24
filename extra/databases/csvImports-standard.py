from flask import Flask, current_app
from flask_sqlalchemy import SQLAlchemy
import csv
import urllib.parse

password = 'Seagate@123'
encoded_password = urllib.parse.quote_plus(password)

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///grocify_sample.sqlite'
# app.config['SQLALCHEMY_DATABASE_URI'] = f'mysql+mysqlconnector://root:{encoded_password}@localhost/grocify_sample'
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'User'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False, unique=True)
    password = db.Column(db.String(255), nullable=False)
    contact = db.Column(db.String(20), nullable=False)
    
class Product(db.Model):
    __tablename__ = 'Product'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    price = db.Column(db.Numeric(10, 2), nullable=False)
    image = db.Column(db.String(255), nullable=False)
    category = db.Column(db.String(255), nullable=False)
    
class Shipping(db.Model):
    __tablename__ = 'Shipping'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=True, default=None)
    full_name = db.Column(db.String(255), nullable=True, default=None)
    street_address = db.Column(db.String(255), nullable=True, default=None)
    city = db.Column(db.String(255), nullable=True, default=None)
    state_province = db.Column(db.String(255), nullable=True, default=None)
    postal_code = db.Column(db.String(255), nullable=True, default=None)
    country = db.Column(db.String(255), nullable=True, default=None)

class Cart(db.Model):
    __tablename__ = 'Cart'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    shipping_id = db.Column(db.Integer, db.ForeignKey('Shipping.id'), nullable=True, default=None)

class CartProduct(db.Model):
    __tablename__ = 'CartProduct'
    cart_id = db.Column(db.Integer, db.ForeignKey('Cart.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'), primary_key=True)

class Order(db.Model):
    __tablename__ = 'Order'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer, db.ForeignKey('User.id'), nullable=False)
    status = db.Column(db.String(255), nullable=False, default='processing')
    total = db.Column(db.Numeric(10, 2), nullable=False)

class OrderProduct(db.Model):
    __tablename__ = 'OrderProduct'
    order_id = db.Column(db.Integer, db.ForeignKey('Order.id'), primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('Product.id'), primary_key=True)

# def read_csv_data(csv_file):
#     with open(csv_file, 'r') as file:
#         reader = csv.DictReader(file)
#         data = [dict(row) for row in reader]
#     return data

# def insert_data(table, data):
#     for row in data:
#         obj = table(**row)
#         db.session.add(obj)
#     db.session.commit()
    
# def initialize_database():
#     db.create_all()

#     # Define a dictionary to map each table to its corresponding CSV file
#     table_csv_mapping = {
#         Cart: 'imports/Cart.csv',
#         CartProduct: 'imports/CartProduct.csv',
#         Order: 'imports/Order.csv',
#         OrderProduct: 'imports/OrderProduct.csv',
#         Product: 'imports/Product.csv',
#         Shipping: 'imports/Shipping.csv',
#         User: 'imports/User.csv',
#     }

#     with current_app.app_context():
#         for table, csv_file in table_csv_mapping.items():
#             data = read_csv_data(csv_file)
#             insert_data(table, data)
            
# # Exception handling
# try:
#     initialize_database()
# except Exception as e:
#     print(f"An error occurred: {str(e)}")
#     # Handle the exception accordingly                

# Define a dictionary to map each table to its corresponding CSV file
table_csv_mapping = {
    Cart: 'extra/imports/Cart.csv',
    CartProduct: 'extra/imports/CartProduct.csv',
    Order: 'extra/imports/Order.csv',
    OrderProduct: 'extra/imports/OrderProduct.csv',
    Product: 'extra/imports/Product.csv',
    Shipping: 'extra/imports/Shipping.csv',
    User: 'extra/imports/User.csv',
}

# Iterate over each table and CSV file
with app.app_context():
    db.create_all()
    for table, csv_file in table_csv_mapping.items():
        # Check if the table is empty
        if db.session.query(table).count() == 0:
            # Read the CSV file
            with open(csv_file, 'r') as file:
                reader = csv.DictReader(file)
                data = [dict(row) for row in reader]

            # Insert the data into the table
            for row in data:
                # Convert blank cells to None
                for key, value in row.items():
                    if value == '':
                        row[key] = None

                obj = table(**row)
                db.session.add(obj)
            db.session.commit()
        else:
            print(f"Skipping import for table {table.__name__}. It is not empty.")