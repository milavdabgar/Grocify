from flask import session, request, render_template, url_for, flash, redirect

from app.admin import bp

from app.forms.admin_data_forms import (
    LocationForm,
    SellerForm,
    Unit,
    CategoryForm,
    ProductForm,
)


@bp.route("/admin/<username>", methods=["GET", "POST"])
def admin(username):
    """
    Admin page handler
    """

    # we need to render all the forms that appear in the modals here
    # and pass it to the templates using a dictionary object which
    # can then be used inside the jinja templates
    location_form = LocationForm()
    seller_form = SellerForm()
    unit_form = Unit()
    category_form = CategoryForm()
    product_form = ProductForm()

    form = {
        "location": location_form,
        "seller": seller_form,
        "unit": unit_form,
        "category": category_form,
        "product": product_form,
    }

    if request.method == "GET":
        if "Username" in session:
            if session["Username"] == username:
                return render_template(
                    "admin/admin_index.html", username=username, form=form
                )
            else:
                print(
                    f"__LOG__ [POSSIBLE BREACH] someone tried to access account of {username}"
                )
                return (
                    "<h1>Nice try hacker!! your tricks not working on this website</h1>"
                )
        else:
            # replace this string with an error handler later
            print(
                f"__LOG__ [POSSIBLE BREACH] someone tried to access account of {username}"
            )
            return "<h1>Nice try hacker!! your tricks not working on this website</h1>"
