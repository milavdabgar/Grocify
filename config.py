#!/usr/bin/python3
import os

# # # Flask configuration
os.environ["YT_API_KEY"] = "AIzaSyDNY4WotVJc8paQgIvHMy83BCYZFXBPwvQ"
os.environ["APP_SECRET_KEY"] = "mjd"

os.environ["DB_HOST"] = "localhost"
os.environ["DB_USER"] = "root"
os.environ["DB_PASSWORD"] = "Seagate@123"
os.environ["DB_DATABASE"] = "fresh_basket"

# MySQL connection config
db_config = {
    'host': os.environ.get('DB_HOST'),
    'user': os.environ.get('DB_USER'),
    'password': os.environ.get('DB_PASSWORD'),
    'database': os.environ.get('DB_DATABASE')
}