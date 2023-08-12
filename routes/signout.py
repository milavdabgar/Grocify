from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, jsonify
import mysql.connector
import bcrypt
import requests
import os
from config import *
from controllers import get_cart_count

bp = Blueprint('signout', __name__)

@bp.route('/signout')
def signout():
    # Clear the session
    session.clear()

    # Redirect to the sign-in page
    return redirect(url_for('signin,signin'))
