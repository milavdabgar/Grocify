from flask import Blueprint, render_template, request, session, redirect, url_for
from app.models import User, Shipping
from app.extensions import db

bp = Blueprint('shipping', __name__)

@bp.route('/shipping', methods=['GET', 'POST'])
def shipping():
    # Check if the user is authenticated
    if 'email' not in session:
        return redirect(url_for('signin.signin'))

    if request.method == 'POST':
        if 'delete_shipping' in request.form:
            # Delete shipping information
            shipping_id = request.form.get('delete_shipping')
            # Delete the shipping information from the database
            Shipping.query.filter_by(id=shipping_id).delete()
            db.session.commit()
            # Redirect the user back to the shipping page
            return redirect(url_for('shipping.shipping'))

        else:
            # Retrieve shipping information from the form
            full_name = request.form.get('full_name')
            street_address = request.form.get('street_address')
            city = request.form.get('city')
            state_province = request.form.get('state_province')
            postal_code = request.form.get('postal_code')
            country = request.form.get('country')

            # Retrieve the user's ID
            user = User.query.filter_by(email=session['email']).first()

            # Insert the shipping information into the shipping table
            shipping = Shipping(user_id=user.id, full_name=full_name, street_address=street_address,
                                city=city, state_province=state_province, postal_code=postal_code, country=country)
            db.session.add(shipping)
            db.session.commit()

            # Retrieve shipping info from database
            shipping_columns = [getattr(Shipping, column_name) for column_name in Shipping.__table__.columns.keys()]   
            shipping_info = db.session.query(*shipping_columns).join(User).filter(
                User.email == session['email']
            ).all()

            # redirect the user back to the shipping page
            return render_template('shipping.html', shipping_info=shipping_info)

    # If it's a GET request, render the shipping information form
    # Retrieve shipping info from database
    shipping_columns = [getattr(Shipping, column_name) for column_name in Shipping.__table__.columns.keys()]   
    shipping_info = db.session.query(*shipping_columns).join(User).filter(
        User.email == session['email']
    ).all()

    return render_template('shipping.html', shipping_info=shipping_info)
