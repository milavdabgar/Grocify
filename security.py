from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_security import Security, SQLAlchemyUserDatastore, UserMixin, RoleMixin

# Create a Flask application and configure it
app = Flask(__name__)
app.config['SECRET_KEY'] = 'your-secret-key'
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///:memory:"
app.config['SECURITY_PASSWORD_SALT'] = 'your-password-salt'

# Initialize the SQLAlchemy extension and create the database models
db = SQLAlchemy(app)

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    fs_uniquifier = db.Column(db.String(64), unique=True)

class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

with app.app_context():
    db.create_all()
# db.create_all()

# Create a SQLAlchemyUserDatastore object using the User and Role models
user_datastore = SQLAlchemyUserDatastore(db, User, Role)

# Initialize the Flask-Security extension
security = Security(app, user_datastore)


# Define your routes
@app.route('/')
def home():
    return 'Hello, Flask-Security!'

# Run the Flask application
if __name__ == '__main__':
    app.run()