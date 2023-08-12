from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, jsonify
import mysql.connector
import bcrypt
import requests
import os
from config import *
from controllers import get_cart_count

bp = Blueprint('admin_panel', __name__)

@bp.route('/admin', methods=['GET'])
def admin_panel():
    # Check if the user is authenticated as an admin
    if 'email' in session and session['email'] == 'admin@frb.com':
        return render_template('admin_panel.html')
    else:
        return redirect(url_for('signin.signin'))
