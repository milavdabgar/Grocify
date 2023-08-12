from flask import Flask, Blueprint, render_template, request, session, redirect, url_for, jsonify
import mysql.connector
import bcrypt
import requests
import os
from config import *
from controllers import get_cart_count

bp = Blueprint('landing', __name__)

@bp.route('/')
def landing():
    return  render_template('landing.html')
