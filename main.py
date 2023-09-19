from application import create_app

app = create_app()

# # Import all the controllers so they are loaded
# print("importing the stuff")
# from application.routes import *


# @app.errorhandler(404)
# def page_not_found(e):
#     # note that we set the 404 status explicitly
#     return render_template("404.html"), 404


# @app.errorhandler(403)
# def not_authorized(e):
#     # note that we set the 403 status explicitly
#     return render_template("403.html"), 403


if __name__ == "__main__":
    app.run(debug=True)
