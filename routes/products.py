from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, jsonify
import mysql.connector
import bcrypt
import requests
import os
from config import *
from controllers import get_cart_count

bp = Blueprint('products', __name__)

@bp.route('/products')
def products():
    # Connect to the MySQL database
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()

    # Retrieve product data from the database
    cursor.execute("SELECT * FROM Product")
    products = cursor.fetchall()

    # Close the cursor and connection
    cursor.close()
    cnx.close()

    # Render the template and pass the product data to it
    cart_count = get_cart_count()
    return render_template('shop.html', products=products, cart_count=cart_count)
