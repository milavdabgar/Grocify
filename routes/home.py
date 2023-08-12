from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, jsonify
import mysql.connector
import bcrypt
import requests
import os
from config import *
from controllers import get_cart_count

bp = Blueprint('home', __name__)

@bp.route('/home')
def home():
    # Check if the user is authenticated
    if 'email' in session:
        if session['email'] == 'admin@frb.com':
            return redirect(url_for('admin_panel.admin_panel'))
        else:
            # For regular users, continue with the existing functionality
            cart_count = get_cart_count()
            return render_template('index.html', cart_count=cart_count)
    else:
        return redirect(url_for('signin.signin'))
