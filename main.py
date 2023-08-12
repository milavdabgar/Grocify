from flask import Flask, render_template
from routes.home import home_bp
from routes.about import about_bp

app = Flask(__name__)

app.register_blueprint(home_bp, url_prefix='/home')
app.register_blueprint(about_bp, url_prefix='/about')

# Define route for the root URL ("/")
# @app.route('/')
# def root():
#     return "Welcome to the root page!"

@app.route('/')
def landing():
    return  render_template('landing.html')
    # return "Welcome to the root page!"


# Run the Flask app
if __name__ == '__main__':
    app.run()
